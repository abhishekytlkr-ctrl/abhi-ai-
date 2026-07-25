"""Deterministic capability metadata for agent tools.

Model output requests an action; it never supplies the authority for that
action.  This module classifies the effects of each built-in tool and applies
run-local integrity gates before dispatch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping
import uuid

from src.provenance import (
    ContextSensitivity,
    ConversationProvenance,
    provenance_from_messages,
)
from src.tool_security import BUILTIN_EMAIL_TOOLS


class ToolEffect(str, Enum):
    READ_PUBLIC = "read_public"
    READ_WORKSPACE = "read_workspace"
    READ_PRIVATE = "read_private"
    WRITE_WORKSPACE = "write_workspace"
    WRITE_PRIVATE = "write_private"
    EXECUTE_CODE = "execute_code"
    BROKERED_NETWORK_READ = "brokered_network_read"
    NETWORK_EGRESS = "network_egress"
    EXTERNAL_SIDE_EFFECT = "external_side_effect"
    UI_SIDE_EFFECT = "ui_side_effect"
    ADMIN_CHANGE = "admin_change"
    DESTRUCTIVE = "destructive"
    USER_INTERACTION = "user_interaction"


class ResultIntegrity(str, Enum):
    SYSTEM = "system"
    ODYSSEUS_UNTRUSTED = "odysseus_untrusted"
    WORKSPACE_UNTRUSTED = "workspace_untrusted"
    EXTERNAL_UNTRUSTED = "external_untrusted"


@dataclass(frozen=True)
class ToolCapabilities:
    effects: frozenset[ToolEffect]
    result_integrity: ResultIntegrity = ResultIntegrity.SYSTEM
    result_sensitivity: ContextSensitivity = ContextSensitivity.PUBLIC
    known: bool = True


def _capabilities(
    *effects: ToolEffect,
    result_integrity: ResultIntegrity = ResultIntegrity.SYSTEM,
    result_sensitivity: ContextSensitivity = ContextSensitivity.PUBLIC,
) -> ToolCapabilities:
    return ToolCapabilities(
        frozenset(effects),
        result_integrity,
        result_sensitivity,
    )


_REGISTRY: dict[str, ToolCapabilities] = {}


def _register(
    names: Iterable[str],
    *effects: ToolEffect,
    result_integrity: ResultIntegrity = ResultIntegrity.SYSTEM,
    result_sensitivity: ContextSensitivity = ContextSensitivity.PUBLIC,
) -> None:
    capabilities = _capabilities(
        *effects,
        result_integrity=result_integrity,
        result_sensitivity=result_sensitivity,
    )
    for name in names:
        if name in _REGISTRY:
            raise RuntimeError(f"Duplicate tool capability classification: {name}")
        _REGISTRY[name] = capabilities


_register(
    {"ask_user", "update_plan"},
    ToolEffect.USER_INTERACTION,
)
_register(
    {
        "list_cached_models",
        "list_cookbook_servers",
        "list_downloads",
        "list_models",
        "list_serve_presets",
        "list_served_models",
        "search_hf_models",
    },
    ToolEffect.READ_PUBLIC,
)
_register(
    {"get_workspace", "glob", "grep", "ls", "read_file"},
    ToolEffect.READ_WORKSPACE,
    result_integrity=ResultIntegrity.WORKSPACE_UNTRUSTED,
    result_sensitivity=ContextSensitivity.WORKSPACE,
)
_register(
    {"web_fetch", "web_search"},
    ToolEffect.BROKERED_NETWORK_READ,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
)
_register(
    {
        "list_emails",
        "read_email",
        "scan_email_unsubscribes",
        "search_emails",
    },
    ToolEffect.READ_PRIVATE,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {
        "list_email_accounts",
        "resolve_contact",
        "search_chats",
        "list_sessions",
        "tail_serve_output",
        "vault_get",
        "vault_search",
    },
    ToolEffect.READ_PRIVATE,
    result_integrity=ResultIntegrity.ODYSSEUS_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {"bash", "manage_bg_jobs", "python"},
    ToolEffect.EXECUTE_CODE,
    result_integrity=ResultIntegrity.WORKSPACE_UNTRUSTED,
    result_sensitivity=ContextSensitivity.WORKSPACE,
)
_register(
    {"apply_patch", "edit_file", "write_file"},
    ToolEffect.WRITE_WORKSPACE,
    result_integrity=ResultIntegrity.WORKSPACE_UNTRUSTED,
    result_sensitivity=ContextSensitivity.WORKSPACE,
)
_register(
    {
        "ai_draft_email_reply",
        "create_document",
        "create_session",
        "draft_email",
        "draft_email_reply",
        "edit_document",
        "manage_calendar",
        "manage_contact",
        "manage_documents",
        "manage_memory",
        "manage_notes",
        "manage_research",
        "manage_session",
        "manage_skills",
        "manage_tasks",
        "pipeline",
        "send_to_session",
        "suggest_document",
        "todowrite",
        "update_document",
    },
    ToolEffect.WRITE_PRIVATE,
    result_integrity=ResultIntegrity.ODYSSEUS_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {"chat_with_model", "ask_teacher"},
    ToolEffect.NETWORK_EGRESS,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
)
_register(
    {"download_attachment"},
    ToolEffect.READ_PRIVATE,
    ToolEffect.WRITE_WORKSPACE,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {"edit_image", "generate_image", "trigger_research"},
    ToolEffect.NETWORK_EGRESS,
    ToolEffect.WRITE_PRIVATE,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {
        "archive_email",
        "bulk_email",
        "mark_email_read",
        "reply_to_email",
        "send_email",
        "unsubscribe_email",
    },
    ToolEffect.EXTERNAL_SIDE_EFFECT,
)
_register(
    {"delete_email"},
    ToolEffect.EXTERNAL_SIDE_EFFECT,
    ToolEffect.DESTRUCTIVE,
)
_register(
    {"ui_control"},
    ToolEffect.UI_SIDE_EFFECT,
)
_register(
    {
        "adopt_served_model",
        "cancel_download",
        "download_model",
        "serve_model",
        "serve_preset",
        "stop_served_model",
        "vault_unlock",
    },
    ToolEffect.ADMIN_CHANGE,
)
_register(
    {
        "manage_endpoints",
        "manage_mcp",
        "manage_settings",
        "manage_tokens",
        "manage_webhooks",
    },
    ToolEffect.ADMIN_CHANGE,
    result_integrity=ResultIntegrity.ODYSSEUS_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_register(
    {"api_call", "app_api"},
    ToolEffect.ADMIN_CHANGE,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)


TOOL_CAPABILITIES: Mapping[str, ToolCapabilities] = MappingProxyType(dict(_REGISTRY))
KNOWN_CAPABILITY_TOOLS = frozenset(TOOL_CAPABILITIES)

_UNKNOWN_CAPABILITIES = _capabilities(
    ToolEffect.READ_PRIVATE,
    ToolEffect.WRITE_WORKSPACE,
    ToolEffect.WRITE_PRIVATE,
    ToolEffect.EXECUTE_CODE,
    ToolEffect.NETWORK_EGRESS,
    ToolEffect.EXTERNAL_SIDE_EFFECT,
    ToolEffect.ADMIN_CHANGE,
    ToolEffect.DESTRUCTIVE,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
    result_sensitivity=ContextSensitivity.PRIVATE,
)
_UNKNOWN_CAPABILITIES = ToolCapabilities(
    _UNKNOWN_CAPABILITIES.effects,
    _UNKNOWN_CAPABILITIES.result_integrity,
    _UNKNOWN_CAPABILITIES.result_sensitivity,
    known=False,
)
_BROWSER_MCP_READ_CAPABILITIES = _capabilities(
    ToolEffect.BROKERED_NETWORK_READ,
    result_integrity=ResultIntegrity.EXTERNAL_UNTRUSTED,
)
_BROWSER_MCP_READ_TOOLS = frozenset(
    {
        "mcp__builtin_browser__browser_console_messages",
        "mcp__builtin_browser__browser_network_requests",
        "mcp__builtin_browser__browser_snapshot",
        "mcp__builtin_browser__browser_take_screenshot",
    }
)


def capabilities_for_tool(tool_name: Any) -> ToolCapabilities:
    """Return deterministic capabilities; malformed and unknown tools fail high."""
    if not isinstance(tool_name, str) or not tool_name:
        return _UNKNOWN_CAPABILITIES
    capabilities = TOOL_CAPABILITIES.get(tool_name)
    if capabilities is not None:
        return capabilities
    if tool_name.startswith("mcp__email__"):
        bare_name = tool_name[len("mcp__email__"):]
        capabilities = TOOL_CAPABILITIES.get(bare_name)
        if bare_name in BUILTIN_EMAIL_TOOLS and capabilities is not None:
            return capabilities
    if tool_name in _BROWSER_MCP_READ_TOOLS:
        return _BROWSER_MCP_READ_CAPABILITIES
    return _UNKNOWN_CAPABILITIES


_PRIVATE_ACTION_READS: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "manage_calendar": frozenset({"list", "list_events", "list_calendars"}),
        "manage_contact": frozenset({"list"}),
        "manage_documents": frozenset({"list", "read", "view", "open", "get"}),
        "manage_memory": frozenset({"list", "search"}),
        "manage_notes": frozenset({"list", "search", "find", "view", "get"}),
        "manage_research": frozenset({"list", "read", "open", "view", "get"}),
        "manage_session": frozenset({"list"}),
        "manage_skills": frozenset({"list", "view", "view_ref", "search"}),
        "manage_tasks": frozenset({"list"}),
    }
)

_PRIVATE_ACTION_WRITES: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "manage_calendar": frozenset(
            {"create_event", "update_event", "delete_event"}
        ),
        "manage_contact": frozenset({"add", "update", "delete"}),
        "manage_documents": frozenset({"delete", "tidy"}),
        "manage_memory": frozenset({"add", "edit", "delete"}),
        "manage_notes": frozenset(
            {"add", "update", "delete", "toggle_item"}
        ),
        "manage_research": frozenset({"delete"}),
        "manage_session": frozenset(
            {
                "switch",
                "open",
                "rename",
                "archive",
                "unarchive",
                "delete",
                "important",
                "unimportant",
                "truncate",
                "fork",
            }
        ),
        "manage_skills": frozenset(
            {"add", "edit", "patch", "publish", "delete"}
        ),
        "manage_tasks": frozenset(
            {"create", "edit", "delete", "pause", "resume", "run"}
        ),
    }
)

_PRIVATE_ACTION_EXTERNAL_RESULTS = frozenset(
    {
        "manage_calendar",
        "manage_contact",
        "manage_research",
    }
)


def _action_from_content(tool_name: str, content: Any) -> str | None:
    """Extract only the deterministic action discriminator from sealed input."""
    if not isinstance(content, str) or not content.strip():
        return None
    if tool_name in {"manage_memory", "manage_session"}:
        action = content.splitlines()[0].strip().casefold()
        return action or None
    try:
        payload = json.loads(content)
    except (TypeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    action = payload.get("action")
    if not isinstance(action, str):
        return None
    action = action.strip().casefold()
    return action or None


def capabilities_for_action(tool_name: Any, content: Any) -> ToolCapabilities:
    """Classify the exact sealed action, failing high on ambiguous multiplexers."""
    base = capabilities_for_tool(tool_name)
    if not isinstance(tool_name, str) or tool_name not in _PRIVATE_ACTION_READS:
        return base

    action = _action_from_content(tool_name, content)
    read_actions = _PRIVATE_ACTION_READS[tool_name]
    if action in read_actions:
        integrity = (
            ResultIntegrity.EXTERNAL_UNTRUSTED
            if tool_name in _PRIVATE_ACTION_EXTERNAL_RESULTS
            else ResultIntegrity.ODYSSEUS_UNTRUSTED
        )
        return _capabilities(
            ToolEffect.READ_PRIVATE,
            result_integrity=integrity,
            result_sensitivity=ContextSensitivity.PRIVATE,
        )
    if action in _PRIVATE_ACTION_WRITES[tool_name]:
        return base

    # Tool schemas do not carry action input, and malformed/unknown actions
    # cannot be trusted as read-only or write-only. Preserve both sides of the
    # authority boundary until the exact known payload exists.
    return _capabilities(
        ToolEffect.READ_PRIVATE,
        ToolEffect.WRITE_PRIVATE,
        result_integrity=ResultIntegrity.ODYSSEUS_UNTRUSTED,
        result_sensitivity=ContextSensitivity.PRIVATE,
    )


POST_UNTRUSTED_BLOCKED_EFFECTS = frozenset(
    {
        ToolEffect.READ_PRIVATE,
        ToolEffect.WRITE_WORKSPACE,
        ToolEffect.WRITE_PRIVATE,
        ToolEffect.EXECUTE_CODE,
        ToolEffect.NETWORK_EGRESS,
        ToolEffect.EXTERNAL_SIDE_EFFECT,
        ToolEffect.UI_SIDE_EFFECT,
        ToolEffect.ADMIN_CHANGE,
        ToolEffect.DESTRUCTIVE,
    }
)
POST_EXTERNAL_BLOCKED_EFFECTS = POST_UNTRUSTED_BLOCKED_EFFECTS

POST_SENSITIVE_BLOCKED_EFFECTS = frozenset(
    {
        ToolEffect.BROKERED_NETWORK_READ,
        ToolEffect.NETWORK_EGRESS,
        ToolEffect.EXTERNAL_SIDE_EFFECT,
    }
)
POST_PRIVATE_BLOCKED_EFFECTS = POST_SENSITIVE_BLOCKED_EFFECTS


@dataclass(frozen=True)
class ToolGateDecision:
    allowed: bool
    reason: str | None = None


_EXTERNAL_MESSAGE_SOURCES = frozenset(
    {
        "injected research context",
        "prefetched search context",
        "research context",
        "web search results",
        "youtube transcript",
    }
)


def messages_contain_external_untrusted_context(messages: Iterable[dict]) -> bool:
    """Detect explicitly labelled external context already present in a run."""
    state = provenance_from_messages(messages)
    if state.external_untrusted_context_seen:
        return True
    # Backward compatibility for saved wrappers created before provenance
    # metadata existed.
    for message in messages or ():
        metadata = message.get("metadata") if isinstance(message, dict) else None
        source = metadata.get("source") if isinstance(metadata, dict) else None
        if (
            isinstance(source, str)
            and source.strip().casefold() in _EXTERNAL_MESSAGE_SOURCES
        ):
            return True
    return False


@dataclass
class ToolRunSecurityContext:
    """Server-owned integrity state for one agent run."""

    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    external_untrusted_context_seen: bool = False
    workspace_untrusted_context_seen: bool = False
    odysseus_untrusted_context_seen: bool = False
    private_data_context_seen: bool = False
    external_sources: list[str] = field(default_factory=list)
    workspace_sources: list[str] = field(default_factory=list)
    odysseus_sources: list[str] = field(default_factory=list)
    private_sources: list[str] = field(default_factory=list)

    @property
    def any_untrusted_context_seen(self) -> bool:
        return bool(
            self.external_untrusted_context_seen
            or self.workspace_untrusted_context_seen
            or self.odysseus_untrusted_context_seen
        )

    @property
    def sensitive_data_context_seen(self) -> bool:
        return bool(
            self.workspace_untrusted_context_seen
            or self.private_data_context_seen
        )

    def to_provenance(self) -> ConversationProvenance:
        return ConversationProvenance(
            external_untrusted_context_seen=self.external_untrusted_context_seen,
            workspace_untrusted_context_seen=self.workspace_untrusted_context_seen,
            odysseus_untrusted_context_seen=self.odysseus_untrusted_context_seen,
            private_data_context_seen=self.private_data_context_seen,
        )

    def merge_provenance(self, state: ConversationProvenance) -> None:
        current = self.to_provenance()
        current.merge(state)
        self.external_untrusted_context_seen = (
            current.external_untrusted_context_seen
        )
        self.workspace_untrusted_context_seen = (
            current.workspace_untrusted_context_seen
        )
        self.odysseus_untrusted_context_seen = (
            current.odysseus_untrusted_context_seen
        )
        self.private_data_context_seen = current.private_data_context_seen

    def decision_for(self, tool_name: Any, content: Any = None) -> ToolGateDecision:
        capabilities = capabilities_for_action(tool_name, content)
        private_blocked = (
            capabilities.effects & POST_SENSITIVE_BLOCKED_EFFECTS
            if self.sensitive_data_context_seen
            else frozenset()
        )
        if not self.any_untrusted_context_seen and not private_blocked:
            return ToolGateDecision(True)
        blocked_effects = (
            capabilities.effects & POST_UNTRUSTED_BLOCKED_EFFECTS
            if self.any_untrusted_context_seen
            else frozenset()
        ) | private_blocked
        if capabilities.known and not blocked_effects:
            return ToolGateDecision(True)
        effects = ", ".join(sorted(effect.value for effect in blocked_effects))
        if not capabilities.known:
            effects = "unknown/high-impact"
        return ToolGateDecision(
            False,
            (
                "Untrusted or sensitive context has already influenced this run. "
                f"Tool '{tool_name}' requires a separate user-authorized action "
                f"because it can cause {effects}."
            ),
        )

    def observe_tool_result(
        self,
        tool_name: Any,
        result: Any,
        content: Any = None,
    ) -> None:
        if not isinstance(result, dict):
            return
        if (
            result.get("blocked")
            or result.get("approval_required")
            or result.get("error")
            or result.get("exit_code") not in (None, 0)
        ):
            return
        capabilities = capabilities_for_action(tool_name, content)
        if capabilities.result_integrity is ResultIntegrity.EXTERNAL_UNTRUSTED:
            self.external_untrusted_context_seen = True
            if isinstance(tool_name, str) and tool_name not in self.external_sources:
                self.external_sources.append(tool_name)
        elif capabilities.result_integrity is ResultIntegrity.WORKSPACE_UNTRUSTED:
            self.workspace_untrusted_context_seen = True
            if isinstance(tool_name, str) and tool_name not in self.workspace_sources:
                self.workspace_sources.append(tool_name)
        elif capabilities.result_integrity is ResultIntegrity.ODYSSEUS_UNTRUSTED:
            self.odysseus_untrusted_context_seen = True
            if isinstance(tool_name, str) and tool_name not in self.odysseus_sources:
                self.odysseus_sources.append(tool_name)
        if capabilities.result_sensitivity is ContextSensitivity.PRIVATE:
            self.private_data_context_seen = True
            if isinstance(tool_name, str) and tool_name not in self.private_sources:
                self.private_sources.append(tool_name)


def blocked_tool_result(tool_name: Any, reason: str) -> tuple[str, dict]:
    return (
        f"{tool_name}: BLOCKED",
        {
            "error": reason,
            "exit_code": 1,
            "blocked": True,
            "policy": "external_untrusted_context",
        },
    )
