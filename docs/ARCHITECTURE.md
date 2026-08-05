# Architecture

> [!NOTE]
> This document is the proposed canonical destination for stable high-level
> architecture facts. It remains subject to maintainer review. Source code,
> tests, and configuration remain authoritative for implementation-sensitive
> behaviour.

## Purpose

This document identifies the stable runtime boundaries and primary ownership
locations used to navigate and extend Odysseus.

It intentionally excludes generated metrics, file-size rankings, refactor
priorities, unresolved investigation findings, and proposed package layouts.

## Runtime structure

| Area | Responsibility |
|---|---|
| `app.py` | FastAPI application composition and primary application entry point |
| `launcher.py` | Application launch support |
| `setup.py` | Native setup workflow |
| `core/` | Authentication, middleware, persistence, sessions, and platform primitives |
| `routes/` | HTTP and API route handlers |
| `src/` | Application orchestration, tools, providers, and runtime helpers |
| `services/` | Domain-oriented service implementations |
| `mcp_servers/` | Built-in MCP server implementations |
| `scripts/` | CLI tools, diagnostics, maintenance, and migration helpers |
| `static/` | No-build browser frontend and bundled assets |
| `tests/` | Automated tests and supporting test infrastructure |

## Subsystem boundaries

| Subsystem | Primary implementation locations |
|---|---|
| Application startup | `app.py`, `src/app_initializer.py`, `core/` |
| Authentication and sessions | `core/auth.py`, `core/middleware.py`, `core/session_manager.py`, `routes/auth_routes.py` |
| Chat and streaming | `routes/chat_routes.py`, `routes/chat_helpers.py`, `src/chat_handler.py`, `src/chat_processor.py`, `src/llm_core.py` |
| Agents and tools | `src/agent_loop.py`, `src/tool_execution.py`, `src/agent_tools/`, `src/tools/`, `src/tool_policy.py`, `src/tool_security.py` |
| Models and providers | `routes/model_routes.py`, `src/model_discovery.py`, `src/model_capabilities.py`, `src/endpoint_resolver.py`, `src/llm_core.py` |
| Cookbook and hardware fit | `routes/cookbook_routes.py`, `routes/cookbook_helpers.py`, `src/cookbook_serve_lifecycle.py`, `services/hwfit/` |
| Search and research | `routes/search_routes.py`, `services/search/`, `routes/research/`, `services/research/`, `src/deep_research.py` |
| Documents and retrieval | `routes/document_routes.py`, `src/document_processor.py`, `src/personal_docs.py`, `src/rag_manager.py`, `src/pdf_runtime.py` |
| Memory and skills | `routes/memory/`, `services/memory/`, `routes/skills_routes.py` |
| Email | `routes/email_routes.py`, `routes/email_helpers.py`, `routes/email_pollers.py`, `mcp_servers/email_server.py` |
| Calendar, contacts, notes, and tasks | `routes/calendar_routes.py`, `routes/contacts/`, `routes/note/`, `routes/task_routes.py`, `src/task_scheduler.py` |
| Media and speech | `routes/gallery/`, `routes/stt_routes.py`, `routes/tts_routes.py`, `services/stt/`, `services/tts/` |
| Persistence and operations | `core/database.py`, `src/runtime_paths.py`, `src/bg_jobs.py`, `routes/backup_routes.py`, `routes/cleanup/` |

## Architectural constraints

- Preserve established import and compatibility paths unless a focused change
  explicitly migrates them.
- Keep HTTP concerns in route modules and reusable domain behaviour in runtime
  or service modules.
- Treat shared persistence, agent orchestration, tool execution, and application
  startup as high-authority boundaries.
- Change one ownership boundary at a time.
- Do not mix structural movement with unrelated feature behaviour.
- Validate affected imports, startup paths, compatibility surfaces, and tests.

## Frontend

The browser frontend is a no-build ES-module application under `static/`.

Its maintained module-level structure is documented in
[`static/js/MODULE_SUMMARY.md`](../static/js/MODULE_SUMMARY.md).

## Investigation and snapshots

Non-canonical investigation material is maintained under [`discovery/`](../discovery/).

The following documents may contain dated observations, metrics, unresolved
questions, or historical planning and must not be treated as specifications:

- [`discovery/system-map.md`](../discovery/system-map.md)
- [`discovery/architecture-runtime-inventory.md`](../discovery/architecture-runtime-inventory.md)

## Documentation authority

- Code, tests, and configuration define implemented behaviour.
- Mature specifications define accepted subsystem behaviour where they exist.
- Following maintainer acceptance, this document will define the high-level
  architecture map.
- Discovery documents preserve evidence and uncertainty but remain
  non-canonical.
