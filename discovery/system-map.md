# Current system map

> [!NOTE]
> This non-canonical discovery map is an evidence guide, not an exhaustive feature catalog or runtime certification. Verify the cited source before relying on a finding. Each section records local implementation observations, evidence locations, confirmed current problems, and unresolved factual questions.

## Navigate the system

- [Startup and application composition](#startup-and-application-composition)
- [Frontend shell and browser interaction](#frontend-shell-and-browser-interaction)
- [Chat, sessions, and streaming](#chat-sessions-and-streaming)
- [Agents, tools, and execution](#agents-tools-and-execution)
- [Models, providers, and local serving](#models-providers-and-local-serving)
- [Search and research](#search-and-research)
- [Documents, retrieval, and personal knowledge](#documents-retrieval-and-personal-knowledge)
- [Memory and skills](#memory-and-skills)
- [Email, calendar, contacts, notes, and tasks](#email-calendar-contacts-notes-and-tasks)
- [Media, speech, and image work](#media-speech-and-image-work)
- [Authentication, secrets, and privileged administration](#authentication-secrets-and-privileged-administration)
- [Persistence, background work, and operations](#persistence-background-work-and-operations)

## Startup and application composition

- **How it works:** [`app.py`](../app.py) creates the application, mounts static assets, constructs shared services, registers route factories, and owns lifespan startup and shutdown. [`src/app_initializer.py`](../src/app_initializer.py) prepares application state; [`core/`](../core/) provides persistence, authentication, middleware, sessions, and platform helpers.

- **Evidence locations:** [`app.py`](../app.py); [`src/app_initializer.py`](../src/app_initializer.py); [`core/database.py`](../core/database.py); [`core/auth.py`](../core/auth.py); [`core/middleware.py`](../core/middleware.py); [`routes/`](../routes/).

- **Known problems:** None recorded by this mapping.

- **Open question:** Which component currently owns startup and shutdown for each long-lived service?

## Frontend shell and browser interaction

- **How it works:** [`static/index.html`](../static/index.html) is served by the root and SPA deep-link routes in [`app.py`](../app.py); [`static/app.js`](../static/app.js), [`static/style.css`](../static/style.css), and [`static/js/`](../static/js/) implement the client surface.

- **Evidence locations:** [`static/index.html`](../static/index.html); [`static/app.js`](../static/app.js); [`static/js/`](../static/js/); [`static/style.css`](../static/style.css); [`app.py`](../app.py) deep-link handlers.

- **Known problems:** The `/backgrounds` route in [`app.py`](../app.py) calls `serve_html_with_nonce` for `static/backgrounds.html`, but that file is absent from [`static/`](../static/). This is a confirmed broken prototype route, not evidence about the rest of the frontend.

- **Open question:** Is `/backgrounds` currently an intentionally supported route or an obsolete prototype?

## Chat, sessions, and streaming

- **How it works:** [`routes/chat_routes.py`](../routes/chat_routes.py) and [`routes/chat_helpers.py`](../routes/chat_helpers.py) coordinate requests, session state, and SSE delivery. [`src/chat_handler.py`](../src/chat_handler.py), [`src/chat_processor.py`](../src/chat_processor.py), [`src/llm_core.py`](../src/llm_core.py), and [`src/session_actions.py`](../src/session_actions.py) provide message preparation, provider interaction, and session operations.

- **Evidence locations:** [`routes/chat_routes.py`](../routes/chat_routes.py); [`routes/chat_helpers.py`](../routes/chat_helpers.py); [`routes/session_routes.py`](../routes/session_routes.py); [`src/chat_handler.py`](../src/chat_handler.py); [`src/chat_processor.py`](../src/chat_processor.py); [`src/llm_core.py`](../src/llm_core.py); [`core/session_manager.py`](../core/session_manager.py).

- **Known problems:** [`src/agent_loop.py`](../src/agent_loop.py) annotates `_resolved_tool_event_name` with `Any` but imports no `Any` and does not enable postponed annotation evaluation. Python evaluates that annotation while importing the module, so this is an import-time defect at the checked baseline.

- **Open question:** No end-to-end provider or browser streaming run was performed for this map.

## Agents, tools, and execution

- **How it works:** [`src/agent_loop.py`](../src/agent_loop.py) drives multi-round tool use. [`src/tool_execution.py`](../src/tool_execution.py) dispatches calls and binds workspace context. [`src/agent_tools/`](../src/agent_tools/) contains individual implementations; [`src/tool_security.py`](../src/tool_security.py) and [`src/tool_policy.py`](../src/tool_policy.py) apply role and request policies. Long-running command work is represented by [`src/bg_jobs.py`](../src/bg_jobs.py).

- **Evidence locations:** [`src/agent_loop.py`](../src/agent_loop.py); [`src/tool_execution.py`](../src/tool_execution.py); [`src/agent_tools/`](../src/agent_tools/); [`src/tool_security.py`](../src/tool_security.py); [`src/tool_policy.py`](../src/tool_policy.py); [`src/tool_schemas.py`](../src/tool_schemas.py); [`src/bg_jobs.py`](../src/bg_jobs.py).

- **Known problems:** The import-time annotation defect above blocks the main agent/tool path. The shell is intentionally not a filesystem or network sandbox; that is an authority boundary, not by itself a vulnerability claim.

- **Open question:** Which native, legacy, and MCP-qualified invocation paths reach each policy gate?

## Models, providers, and local serving

- **How it works:** Model routes delegate to discovery, capabilities, endpoint resolution, and LLM core modules. Cookbook routes and hardware-fit services handle model lifecycle and local-serving support.

- **Evidence locations:** [`routes/model_routes.py`](../routes/model_routes.py); [`src/model_discovery.py`](../src/model_discovery.py); [`src/model_capabilities.py`](../src/model_capabilities.py); [`src/endpoint_resolver.py`](../src/endpoint_resolver.py); [`src/llm_core.py`](../src/llm_core.py); [`routes/cookbook_routes.py`](../routes/cookbook_routes.py); [`src/cookbook_serve_lifecycle.py`](../src/cookbook_serve_lifecycle.py); [`services/hwfit/`](../services/hwfit/).

- **Known problems:** None recorded by this mapping.

- **Open question:** Which endpoint inputs are administrator-created and permitted to use private provider addresses?

## Search and research

- **How it works:** HTTP search routes use [`services/search/`](../services/search/); research is exposed through [`routes/research/`](../routes/research/) and implemented in [`services/research/`](../services/research/), [`src/deep_research.py`](../src/deep_research.py), and related helpers. [`src/search/`](../src/search/) remains an import-compatibility layer for callers not yet moved to `services.search`.

- **Evidence locations:** [`routes/search_routes.py`](../routes/search_routes.py); [`services/search/`](../services/search/); [`routes/research/research_routes.py`](../routes/research/research_routes.py); [`services/research/`](../services/research/); [`src/deep_research.py`](../src/deep_research.py); [`src/search/`](../src/search/).

- **Known problems:** None recorded by this mapping.

- **Open question:** No live provider request was made; provider configuration and network access remain unverified.

## Documents, retrieval, and personal knowledge

- **How it works:** Document routes coordinate upload handling, document processing, and editor actions. Personal-document and RAG modules use Chroma and embedding clients. PDF viewing uses the optional-dependency loader in [`src/pdf_runtime.py`](../src/pdf_runtime.py); form extraction and filling live separately in [`src/pdf_forms.py`](../src/pdf_forms.py) and [`src/pdf_form_doc.py`](../src/pdf_form_doc.py).

- **Evidence locations:** [`routes/document_routes.py`](../routes/document_routes.py); [`src/upload_handler.py`](../src/upload_handler.py); [`src/document_processor.py`](../src/document_processor.py); [`src/document_actions.py`](../src/document_actions.py); [`src/personal_docs.py`](../src/personal_docs.py); [`src/rag_manager.py`](../src/rag_manager.py); [`src/embeddings.py`](../src/embeddings.py); [`src/pdf_runtime.py`](../src/pdf_runtime.py); [`src/pdf_forms.py`](../src/pdf_forms.py); [`src/pdf_form_doc.py`](../src/pdf_form_doc.py).

- **Known problems:** PDF viewing/runtime loading and PDF form processing are separate implementations. That separation is confirmed and intentional in the source; it is not a defect without a reported behavioural failure.

- **Open question:** Optional PDF dependencies and representative uploaded documents were not exercised.

## Memory and skills

- **How it works:** Memory routes use [`services/memory/`](../services/memory/) and vector helpers. Skills are exposed through [`routes/skills_routes.py`](../routes/skills_routes.py), stored and managed in [`services/memory/skills.py`](../services/memory/skills.py), and may be imported through [`services/memory/skill_importer.py`](../services/memory/skill_importer.py).

- **Evidence locations:** [`routes/memory/memory_routes.py`](../routes/memory/memory_routes.py); [`services/memory/`](../services/memory/); [`src/memory.py`](../src/memory.py); [`src/memory_vector.py`](../src/memory_vector.py); [`routes/skills_routes.py`](../routes/skills_routes.py); [`services/memory/skills.py`](../services/memory/skills.py); [`services/memory/skill_importer.py`](../services/memory/skill_importer.py).

- **Known problems:** None recorded by this mapping.

- **Open question:** Which imported skill content can reach execution-capable paths, and which validation occurs before that point?

## Email, calendar, contacts, notes, and tasks

- **How it works:** Dedicated route modules own email, CalDAV calendar, CardDAV contacts, notes, and tasks. Supporting modules include email helpers and pollers, CalDAV sync and writeback, and the task scheduler.

- **Evidence locations:** [`routes/email_routes.py`](../routes/email_routes.py); [`routes/calendar_routes.py`](../routes/calendar_routes.py); [`routes/contacts/contacts_routes.py`](../routes/contacts/contacts_routes.py); [`routes/note/note_routes.py`](../routes/note/note_routes.py); [`routes/task_routes.py`](../routes/task_routes.py); [`routes/assistant_routes.py`](../routes/assistant_routes.py); [`src/caldav_sync.py`](../src/caldav_sync.py); [`src/caldav_writeback.py`](../src/caldav_writeback.py); [`src/task_scheduler.py`](../src/task_scheduler.py).

- **Known problems:** None recorded by this mapping.

- **Open question:** External account behaviour, writeback, and delivery require controlled credentials and are not runtime-validated here.

## Media, speech, and image work

- **How it works:** Gallery and image routes coordinate media features. Service modules own speech and media integrations; [`src/generated_images.py`](../src/generated_images.py) and [`src/visual_report.py`](../src/visual_report.py) support artifact handling and presentation.

- **Evidence locations:** [`routes/gallery/gallery_routes.py`](../routes/gallery/gallery_routes.py); [`routes/stt_routes.py`](../routes/stt_routes.py); [`routes/tts_routes.py`](../routes/tts_routes.py); [`src/generated_images.py`](../src/generated_images.py); [`services/stt/`](../services/stt/); [`services/tts/`](../services/tts/); [`services/faces/`](../services/faces/); [`src/visual_report.py`](../src/visual_report.py).

- **Known problems:** None recorded by this mapping.

- **Open question:** Hardware- and provider-dependent media workflows were not exercised.

## Authentication, secrets, and privileged administration

- **How it works:** [`core/auth.py`](../core/auth.py) and [`core/middleware.py`](../core/middleware.py) provide identity and request gates. [`src/secret_storage.py`](../src/secret_storage.py) encrypts application-managed database secrets with a local Fernet key. Vault handling is separate: [`routes/vault_routes.py`](../routes/vault_routes.py) and [`src/tools/vault.py`](../src/tools/vault.py) invoke the Bitwarden CLI and persist its session data in the application data area.

- **Evidence locations:** [`core/auth.py`](../core/auth.py); [`core/middleware.py`](../core/middleware.py); [`routes/auth_routes.py`](../routes/auth_routes.py); [`routes/api_token_routes.py`](../routes/api_token_routes.py); [`src/secret_storage.py`](../src/secret_storage.py); [`routes/vault_routes.py`](../routes/vault_routes.py); [`src/tools/vault.py`](../src/tools/vault.py); [`routes/admin_wipe/admin_wipe_routes.py`](../routes/admin_wipe/admin_wipe_routes.py).

- **Known problems:** Vault-command handling and local application secret storage are distinct paths with different storage mechanisms. This is a source-confirmed boundary, not evidence that either path is compromised.

- **Open question:** What are the current confidentiality, ownership, rotation, and backup semantics for vault session data?

## Persistence, background work, and operations

- **How it works:** SQLite models and persistence are centred in [`core/database.py`](../core/database.py); managers use application data paths. The scheduler and background-job monitor can continue work outside a live browser request. Operational routes cover cleanup, backup, and administrative wipe; the repository also provides a backup script and user documentation.

- **Evidence locations:** [`core/database.py`](../core/database.py); [`src/runtime_paths.py`](../src/runtime_paths.py); [`src/task_scheduler.py`](../src/task_scheduler.py); [`src/bg_jobs.py`](../src/bg_jobs.py); [`src/bg_monitor.py`](../src/bg_monitor.py); [`routes/backup_routes.py`](../routes/backup_routes.py); [`routes/cleanup/cleanup_routes.py`](../routes/cleanup/cleanup_routes.py); [`routes/admin_wipe/admin_wipe_routes.py`](../routes/admin_wipe/admin_wipe_routes.py); [`scripts/odysseus-backup`](../scripts/odysseus-backup); [`docs/backup-restore.md`](../docs/backup-restore.md).

- **Known problems:** None recorded by this mapping.

- **Open question:** What current behaviour applies to background execution, cancellation, retries, and authority inheritance?
