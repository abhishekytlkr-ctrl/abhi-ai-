# Safety boundaries

> [!IMPORTANT]
> This non-canonical discovery map records code-grounded safeguards, confirmed risks or gaps, and unverified behaviour. Broad authority does not by itself establish a vulnerability. Verify the cited source before relying on a finding. No destructive test, external connection, or real credential was used for this map.

## Navigate the boundaries

- [Shell and subprocess execution](#shell-and-subprocess-execution)
- [Filesystem access and workspace confinement](#filesystem-access-and-workspace-confinement)
- [Agent-controlled tool dispatch](#agent-controlled-tool-dispatch)
- [MCP and external tool servers](#mcp-and-external-tool-servers)
- [Outbound network requests and URL validation](#outbound-network-requests-and-url-validation)
- [Secrets, credentials, and vault sessions](#secrets-credentials-and-vault-sessions)
- [Authentication and privileged administration](#authentication-and-privileged-administration)
- [Deletion, wipe, backup, and restore](#deletion-wipe-backup-and-restore)
- [Background jobs and unattended task execution](#background-jobs-and-unattended-task-execution)

## Shell and subprocess execution

- **Boundary:** Shell routes, agent `bash` and `python` tools, local model serving, and detached background jobs.

- **Available authority:** Commands run as the application process user and can create child processes.

- **User-controlled inputs:** Direct shell requests, model-produced tool arguments, scheduled-task prompts, and model-serving configuration.

- **Current safeguards:** Agent dispatch applies owner/admin checks and tool policy; process helpers use timeouts or bounded background-job lifecycle where implemented.

- **Confirmed risks or gaps:** Intentional authority with a confirmed gap: the agent shell starts in its workspace but is not sandboxed to it, and has no egress sandbox. This is documented in source and the threat model; it is not a newly demonstrated bypass.

- **Unverified behaviour:** Role-gate and disabled-tool outcomes, direct shell-route behaviour, and timeout, cancellation, and output handling for foreground and detached processes remain unverified.

## Filesystem access and workspace confinement

- **Boundary:** Agent read, write, patch, listing, glob, and grep tools.

- **Available authority:** Read and modify files within active workspace confinement or fallback allowlisted roots.

- **User-controlled inputs:** Tool paths, patches, file contents, search patterns, and workspace selection passed into the tool dispatcher.

- **Current safeguards:** [`src/tool_execution.py`](../src/tool_execution.py) resolves paths, blocks sensitive subpaths, applies allowlist containment, and tightens paths to the active workspace when one is bound. File tools use those resolvers.

- **Confirmed risks or gaps:** Intentional authority with safeguards. The file-tool policy does not sandbox the shell; treating a workspace as a whole-process containment boundary would be incorrect.

- **Unverified behaviour:** Traversal, symlink, sensitive-name, absolute-path, and workspace-switch behaviour remains unverified.

## Agent-controlled tool dispatch

- **Boundary:** Model output becomes native or parsed tool calls and is dispatched by the agent loop.

- **Available authority:** The authority of every enabled tool, including privileged built-ins and external tools.

- **User-controlled inputs:** Chat content, attached/retrieved content that may influence the model, tool arguments, per-request tool selection, and policy toggles.

- **Current safeguards:** [`src/tool_security.py`](../src/tool_security.py) blocks protected tools for non-admin users and fails closed for malformed tool names; [`src/tool_policy.py`](../src/tool_policy.py) supports disabled and guide-only policy; prompt-security helpers label untrusted context.

- **Confirmed risks or gaps:** Credible risk requiring verification: aliases, legacy text tools, native function calls, and MCP-qualified names must all reach the same policy outcome. The code has specific alias handling for email/MCP names, which makes this a sensitive compatibility seam.

- **Unverified behaviour:** The current policy outcomes for owner role, request mode, disabled state, native versus parsed invocation, qualified aliases, and external-content entry points remain unverified.

## MCP and external tool servers

- **Boundary:** Configured MCP servers and their tools are exposed to the agent through the MCP manager and routes.

- **Available authority:** Depends on the server: external network access, local process access, messaging, or data mutation may be delegated outside the application.

- **User-controlled inputs:** Server configuration, remote OAuth completion, tool arguments, and model-selected MCP calls.

- **Current safeguards:** MCP routes are registered through [`routes/mcp_routes.py`](../routes/mcp_routes.py); MCP-qualified tools are denied to non-admin users by [`src/tool_security.py`](../src/tool_security.py). OAuth state and token persistence are handled in [`src/mcp_oauth.py`](../src/mcp_oauth.py).

- **Confirmed risks or gaps:** Credible risk requiring verification: an MCP server authority is broader than the application can infer from its tool name. This map does not establish a trust or approval model for server installation and individual tool invocation.

- **Unverified behaviour:** Server onboarding, credential storage, server-origin trust, OAuth callback deployment, tool disablement, and invocation audit behaviour remain unverified.

## Outbound network requests and URL validation

- **Boundary:** Search/content fetch, research, webhooks, skill import, provider endpoints, and other HTTP clients.

- **Available authority:** The application can make outbound requests from its network position.

- **User-controlled inputs:** Search/fetch URLs, imported skill URLs, webhook configuration, and some endpoint settings.

- **Current safeguards:** [`src/url_security.py`](../src/url_security.py) validates untrusted public HTTP URLs and fails closed on unsuitable schemes or private addresses. [`services/search/content.py`](../services/search/content.py) resolves and rejects non-public hosts, pins resolved addresses for fetches, caps bodies, and limits redirects.

- **Confirmed risks or gaps:** Intentional split: administrator-created model endpoints may target private providers, while untrusted URLs use public-address checks. That distinction is required for self-hosted deployments but needs explicit call-site review.

- **Unverified behaviour:** The URL-source classification for outbound clients and the current handling of redirects and DNS changes remain unverified.

## Secrets, credentials, and vault sessions

- **Boundary:** Application-managed encrypted secrets, API keys, provider credentials, and Bitwarden/Vaultwarden CLI sessions.

- **Available authority:** Credentials unlock remote providers and connected personal services.

- **User-controlled inputs:** Administrative configuration, login/unlock requests, imported settings, and agent vault tool arguments.

- **Current safeguards:** [`src/secret_storage.py`](../src/secret_storage.py) uses a locally stored Fernet key with restrictive permissions for supported database secrets. Vault routes require an administrator, avoid passing master passwords in command arguments, and set restrictive permissions on the vault-session file.

- **Confirmed risks or gaps:** Confirmed current boundary: vault session data is persisted through the vault path, not through [`src/secret_storage.py`](../src/secret_storage.py). This is an unresolved question about current security semantics, not a confirmed exposure.

- **Unverified behaviour:** Current encryption-at-rest, owner scope, rotation, lock/logout, backup/restore, and log/tool-result exposure behaviour remains unverified.

## Authentication and privileged administration

- **Boundary:** Session authentication, API tokens, privileged routes, and internal tool loopback.

- **Available authority:** Administrative identity can access execution, settings, integrations, data deletion, and secrets.

- **User-controlled inputs:** Login/signup data, session cookies, API tokens, authentication configuration, and requests to privileged routes.

- **Current safeguards:** [`core/auth.py`](../core/auth.py), [`core/middleware.py`](../core/middleware.py), and route-level checks establish identity and administrator gates. [`app.py`](../app.py) warns when localhost bypass is configured; [`SECURITY.md`](../SECURITY.md) documents deployment requirements.

- **Confirmed risks or gaps:** Intentional authority with safeguards. Security depends on deployments keeping authentication enabled and internal services private; this map does not audit reverse-proxy or environment configuration.

- **Unverified behaviour:** Setup, anonymous, non-admin, admin, token, and internal-loopback behaviour, including privileged-route gate consistency, remains unverified.

## Deletion, wipe, backup, and restore

- **Boundary:** Administrative wipe, cleanup, backup import/export, and the backup restore command.

- **Available authority:** Delete or replace user data and credentials.

- **User-controlled inputs:** Administrative HTTP requests, cleanup choices, backup payloads, archive paths, and restore command options.

- **Current safeguards:** Administrative wipe routes use the administrative boundary. Cleanup exposes a preview route before mutation. The documented backup tool requires explicit restore confirmation, stages the old data directory, and validates archive members before extraction.

- **Confirmed risks or gaps:** Intentional destructive authority. Backup archives contain secrets by design, as documented in [`docs/backup-restore.md`](../docs/backup-restore.md); this is an operator confidentiality responsibility, not a code defect established here.

- **Unverified behaviour:** Role-gate, confirmation, archive-rejection, staged-recovery, and owner-isolation behaviour remains unverified. No destructive runtime test was performed.

## Background jobs and unattended task execution

- **Boundary:** Scheduled tasks, background-job monitor, startup tasks, and notification/delivery work that continue without an active browser request.

- **Available authority:** Scheduled agent work can obtain model access and, for eligible owners, shell and file tools; task output can interact with connected services.

- **User-controlled inputs:** Stored task prompt, schedule, model/crew selection, enabled-tool configuration, output target, and prior persisted state.

- **Current safeguards:** [`src/task_scheduler.py`](../src/task_scheduler.py) serializes execution, records task runs, associates work with an owner, and applies the agent owner-based tool gate. [`src/bg_jobs.py`](../src/bg_jobs.py) keeps bounded state and can terminate overlong subprocess jobs.

- **Confirmed risks or gaps:** Credible risk requiring verification: authority is inherited and exercised later, so changes to roles, task configuration, and disabled tools must be checked at execution time rather than assumed from task creation.

- **Unverified behaviour:** Creation, editing, role-change, scheduling, cancellation, restart-recovery, and execution behaviour remains unverified, including whether current policy is re-evaluated before privileged action.
