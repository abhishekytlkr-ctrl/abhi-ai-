"""Opaque, exact, one-use approvals for model-requested tool actions.

Approval authority lives only in this process. The browser receives an opaque
identifier plus a non-authoritative display copy; the stored record retains the
exact tool input and binding fields. Resuming a turn executes that stored
action, never a model re-emission or a natural-language "yes".
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import threading
import time
from dataclasses import dataclass, field
from typing import Any

from src.agent_run_policy import AgentRunMode, parse_agent_run_mode
from src.tool_capabilities import ToolCapabilities, capabilities_for_tool


DEFAULT_APPROVAL_TTL_SECONDS = 10 * 60


def _normalized_owner(owner: Any) -> str:
    return str(owner or "").strip().casefold()


def _normalized_workspace(workspace: Any) -> str:
    if not isinstance(workspace, str) or not workspace.strip():
        return ""
    return os.path.realpath(os.path.expanduser(workspace))


def _canonical_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _binding_payload(
    *,
    owner: Any,
    session_id: Any,
    origin_run_id: Any,
    tool_name: Any,
    content: Any,
    workspace: Any,
    security_mode: Any,
    external_untrusted_context_seen: bool,
    effects: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "owner": _normalized_owner(owner),
        "session_id": str(session_id or ""),
        "origin_run_id": str(origin_run_id or ""),
        "tool_name": str(tool_name or ""),
        "content": str(content or ""),
        "workspace": _normalized_workspace(workspace),
        "security_mode": parse_agent_run_mode(security_mode).value,
        "external_untrusted_context_seen": bool(external_untrusted_context_seen),
        "effects": list(effects),
    }


@dataclass(frozen=True)
class PendingToolApproval:
    approval_id: str
    owner: str
    session_id: str
    origin_run_id: str
    tool_name: str
    content: str
    workspace: str
    security_mode: AgentRunMode
    external_untrusted_context_seen: bool
    effects: tuple[str, ...]
    digest: str
    created_at: float
    expires_at: float

    def public_payload(self, *, reason: str | None = None) -> dict[str, Any]:
        return {
            "kind": "tool_approval",
            "approval_id": self.approval_id,
            "question": "Allow this exact action once?",
            "description": reason or "The action is outside this thread's automatic authority.",
            "options": [
                {
                    "label": "Allow once",
                    "value": "approve",
                    "description": "Execute only the sealed action shown here.",
                },
                {
                    "label": "Deny",
                    "value": "deny",
                    "description": "Do not execute it.",
                },
            ],
            "action": {
                "tool": self.tool_name,
                # Display data, not authority. Show the complete sealed input
                # so the user never approves hidden trailing lines.
                "content": self.content,
                "digest": self.digest[:16],
                "effects": list(self.effects),
                "workspace": self.workspace or None,
            },
        }


@dataclass
class ExactToolApproval:
    """A consumed approval grant; a dispatcher can claim it exactly once."""

    pending: PendingToolApproval
    _claimed: bool = field(default=False, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    def _matches_unlocked(
        self,
        *,
        owner: Any,
        session_id: Any,
        tool_name: Any,
        content: Any,
        workspace: Any,
        security_mode: Any,
    ) -> bool:
        if self._claimed:
            return False
        current_effects = tuple(
            sorted(
                effect.value
                for effect in capabilities_for_tool(tool_name).effects
            )
        )
        if current_effects != self.pending.effects:
            return False
        expected = _binding_payload(
            owner=owner,
            session_id=session_id,
            origin_run_id=self.pending.origin_run_id,
            tool_name=tool_name,
            content=content,
            workspace=workspace,
            security_mode=security_mode,
            external_untrusted_context_seen=self.pending.external_untrusted_context_seen,
            effects=self.pending.effects,
        )
        return _canonical_digest(expected) == self.pending.digest

    def matches(
        self,
        *,
        owner: Any,
        session_id: Any,
        tool_name: Any,
        content: Any,
        workspace: Any,
        security_mode: Any,
    ) -> bool:
        """Validate a binding for safe presentation without consuming it."""
        with self._lock:
            return self._matches_unlocked(
                owner=owner,
                session_id=session_id,
                tool_name=tool_name,
                content=content,
                workspace=workspace,
                security_mode=security_mode,
            )

    def claim(
        self,
        *,
        owner: Any,
        session_id: Any,
        tool_name: Any,
        content: Any,
        workspace: Any,
        security_mode: Any,
    ) -> bool:
        with self._lock:
            if not self._matches_unlocked(
                owner=owner,
                session_id=session_id,
                tool_name=tool_name,
                content=content,
                workspace=workspace,
                security_mode=security_mode,
            ):
                return False
            self._claimed = True
            return True


class ToolApprovalStore:
    """Thread-safe pending approval registry with destructive consumption."""

    def __init__(self, *, ttl_seconds: int = DEFAULT_APPROVAL_TTL_SECONDS):
        self._ttl_seconds = max(1, int(ttl_seconds))
        self._pending: dict[str, PendingToolApproval] = {}
        self._lock = threading.Lock()

    def _purge_expired_locked(self, now: float) -> None:
        expired = [
            approval_id
            for approval_id, pending in self._pending.items()
            if pending.expires_at <= now
        ]
        for approval_id in expired:
            self._pending.pop(approval_id, None)

    def create(
        self,
        *,
        owner: Any,
        session_id: Any,
        origin_run_id: Any,
        tool_name: Any,
        content: Any,
        workspace: Any,
        security_mode: Any,
        external_untrusted_context_seen: bool,
        capabilities: ToolCapabilities,
    ) -> PendingToolApproval:
        now = time.time()
        effects = tuple(sorted(effect.value for effect in capabilities.effects))
        payload = _binding_payload(
            owner=owner,
            session_id=session_id,
            origin_run_id=origin_run_id,
            tool_name=tool_name,
            content=content,
            workspace=workspace,
            security_mode=security_mode,
            external_untrusted_context_seen=external_untrusted_context_seen,
            effects=effects,
        )
        pending = PendingToolApproval(
            approval_id=secrets.token_urlsafe(32),
            owner=payload["owner"],
            session_id=payload["session_id"],
            origin_run_id=payload["origin_run_id"],
            tool_name=payload["tool_name"],
            content=payload["content"],
            workspace=payload["workspace"],
            security_mode=parse_agent_run_mode(payload["security_mode"]),
            external_untrusted_context_seen=payload["external_untrusted_context_seen"],
            effects=effects,
            digest=_canonical_digest(payload),
            created_at=now,
            expires_at=now + self._ttl_seconds,
        )
        with self._lock:
            self._purge_expired_locked(now)
            self._pending[pending.approval_id] = pending
        return pending

    def consume(
        self,
        approval_id: Any,
        *,
        decision: Any,
        owner: Any,
        session_id: Any,
    ) -> ExactToolApproval | None:
        now = time.time()
        with self._lock:
            self._purge_expired_locked(now)
            pending = self._pending.pop(str(approval_id or ""), None)
        if pending is None:
            return None
        if (
            pending.owner != _normalized_owner(owner)
            or pending.session_id != str(session_id or "")
        ):
            return None
        if str(decision or "").strip().lower() != "approve":
            return None
        return ExactToolApproval(pending)

    def peek(self, approval_id: Any) -> PendingToolApproval | None:
        now = time.time()
        with self._lock:
            self._purge_expired_locked(now)
            return self._pending.get(str(approval_id or ""))


tool_approval_store = ToolApprovalStore()
