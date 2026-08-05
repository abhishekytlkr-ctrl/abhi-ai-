# Architecture runtime inventory

> [!WARNING]
> This document is a dated structural snapshot, not a canonical runtime specification.
> Counts, paths, and implementation details may drift as the repository changes.
> Verify implementation-sensitive claims against the current code and tests.

- **Branch:** `discovery`
- **Commit:** `c762efe1c97a`
- **Generated:** `2026-07-28T05:38:14+01:00`
- **Historical context:** readability and refactor planning in [#4071](https://github.com/odysseus-dev/odysseus/issues/4071) and [#4082](https://github.com/odysseus-dev/odysseus/issues/4082)

## Disposition

> [!NOTE]
> Reviewed for documentation classification. Stable runtime structure and
> subsystem ownership have been transferred to the proposed canonical
> destination, [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md), for
> maintainer review.
>
> This document retains dated metrics, rankings, investigation context,
> refactor-sensitive observations, and historical planning. Those contents are
> non-canonical and belong under `discovery/`.

| Content | Authority and destination |
|---|---|
| Stable runtime structure | Proposed canonical destination: `docs/ARCHITECTURE.md` |
| Stable subsystem boundaries | Proposed canonical destination: `docs/ARCHITECTURE.md` |
| Frontend module organization | `static/js/MODULE_SUMMARY.md` |
| Counts, line totals, and rankings | This non-canonical inventory |
| Investigation context and open questions | `discovery/` |
| Refactor options and prioritization | Issues, Plane, or non-canonical discovery material |

The transfer preserves the stable facts without promoting generated metrics or
historical prioritization into canonical documentation.

## Purpose

This inventory provides a reviewable map of the current repository structure,
large runtime modules, major subsystem boundaries, and refactor-sensitive areas.

It does not:

- define accepted subsystem behaviour;
- certify runtime correctness;
- prescribe a committed refactor sequence;
- replace focused specifications, tests, or source review.

For cross-cutting implementation evidence, see the [discovery maps](./README.md).

## Top-level runtime structure

| Area | Role |
|---|---|
| `app.py` | FastAPI application composition and entry point |
| `launcher.py` | Application launch support |
| `setup.py` | Native setup workflow |
| `core/` | Authentication, middleware, persistence, sessions, and platform primitives |
| `routes/` | HTTP and API route handlers |
| `src/` | Application services, orchestration, tools, providers, and runtime helpers |
| `services/` | Domain-oriented service packages |
| `mcp_servers/` | Built-in MCP server implementations |
| `scripts/` | CLI tools, diagnostics, maintenance, and migration helpers |
| `static/` | No-build browser frontend and bundled assets |
| `tests/` | Automated test suite and supporting test infrastructure |

## Directory snapshot

| Directory | Tracked files | Tracked Python files | Direct subdirectories |
|---|---:|---:|---|
| `src/` | 143 | 143 | `agent_tools/`, `model_capability_readers/`, `search/`, `tools/` |
| `routes/` | 73 | 73 | `admin_wipe/`, `cleanup/`, `compare/`, `contacts/`, `gallery/`, `history/`, `memory/`, `note/`, `research/` |
| `core/` | 11 | 11 | None |
| `services/` | 42 | 40 | `docs/`, `faces/`, `hwfit/`, `memory/`, `research/`, `search/`, `shell/`, `stt/`, `tts/`, `youtube/` |
| `mcp_servers/` | 5 | 5 | None |
| `scripts/` | 44 | 17 | `_completion/`, `_lib/`, `demo_email/` |
| `static/js/` | 154 | 0 | `calendar/`, `color/`, `compare/`, `editor/`, `emailLibrary/`, `markdown/`, `model/`, `research/`, `util/` |
| `tests/` | 768 | 758 | `cli/`, `helpers/`, `streaming/`, `tools/` |

> [!NOTE]
> Counts in this table use `git ls-files`, so generated caches, virtual
> environments, and other untracked local files are excluded.

## Largest backend modules

Large files are review signals, not proof that a module should be split.
Coupling, ownership, import compatibility, tests, and runtime authority matter more
than line count alone.

| Rank | File | Lines | Classes | Top-level functions | Review signal |
|---:|---|---:|---:|---:|---|
| 1 | `routes/email_routes.py` | 6032 | 1 | 58 | High |
| 2 | `src/agent_loop.py` | 5248 | 0 | 63 | High |
| 3 | `routes/cookbook_routes.py` | 4545 | 0 | 16 | High |
| 4 | `mcp_servers/email_server.py` | 2920 | 0 | 77 | High |
| 5 | `src/llm_core.py` | 2895 | 3 | 85 | High |
| 6 | `src/builtin_actions.py` | 2845 | 2 | 27 | High |
| 7 | `routes/model_routes.py` | 2743 | 0 | 65 | High |
| 8 | `src/task_scheduler.py` | 2627 | 1 | 8 | Medium |
| 9 | `core/database.py` | 2562 | 28 | 67 | High |
| 10 | `routes/gallery/gallery_routes.py` | 2325 | 0 | 16 | Medium |
| 11 | `routes/chat_routes.py` | 2063 | 0 | 18 | Medium |
| 12 | `routes/shell_routes.py` | 1971 | 1 | 21 | Medium |
| 13 | `src/visual_report.py` | 1933 | 0 | 11 | Medium |
| 14 | `routes/email_helpers.py` | 1888 | 3 | 48 | Medium |
| 15 | `routes/document_routes.py` | 1810 | 0 | 5 | Medium |
| 16 | `src/tools/cookbook.py` | 1705 | 0 | 34 | Medium |
| 17 | `routes/calendar_routes.py` | 1667 | 2 | 19 | Medium |
| 18 | `routes/skills_routes.py` | 1662 | 3 | 19 | Medium |
| 19 | `src/tool_schemas.py` | 1595 | 0 | 3 | Medium |
| 20 | `routes/email_pollers.py` | 1551 | 0 | 23 | Medium |

The largest current backend concentrations include:

- email routing and helper logic;
- agent-loop orchestration;
- Cookbook lifecycle and serving logic;
- provider and model routing;
- task scheduling;
- shared database models and persistence helpers.

These areas require focused ownership and compatibility analysis before structural
changes are attempted.

## Largest frontend modules

| Rank | File | Lines |
|---:|---|---:|
| 1 | `static/style.css` | 41132 |
| 2 | `static/js/document.js` | 11200 |
| 3 | `static/js/emailLibrary.js` | 8505 |
| 4 | `static/js/slashCommands.js` | 6520 |
| 5 | `static/js/chat.js` | 6001 |
| 6 | `static/js/settings.js` | 5819 |
| 7 | `static/js/notes.js` | 5365 |
| 8 | `static/app.js` | 4681 |
| 9 | `static/js/cookbookRunning.js` | 4433 |
| 10 | `static/js/galleryEditor.js` | 4386 |
| 11 | `static/js/cookbookServe.js` | 4305 |
| 12 | `static/js/calendar.js` | 3722 |
| 13 | `static/js/cookbook.js` | 3677 |
| 14 | `static/js/sessions.js` | 3665 |
| 15 | `static/js/documentLibrary.js` | 3422 |
| 16 | `static/js/tasks.js` | 3187 |
| 17 | `static/js/admin.js` | 3144 |
| 18 | `static/js/gallery.js` | 2958 |
| 19 | `static/js/cookbook-hwfit.js` | 2826 |
| 20 | `static/js/chatRenderer.js` | 2808 |

The browser frontend remains a no-build ES-module application. Its current source
tree is authoritative; the maintained structural summary is available in
[`static/js/MODULE_SUMMARY.md`](../static/js/MODULE_SUMMARY.md).

CSS modularization remains tracked separately in
[#2617](https://github.com/odysseus-dev/odysseus/issues/2617).

## Major subsystem boundaries

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

For a broader evidence map, see
[`system-map.md`](./system-map.md).

## Refactor-sensitive areas

### Shared persistence

`core/database.py` is a central dependency containing models and shared persistence
helpers. Changes can affect routes, services, background work, tests, migrations,
and import compatibility.

A split should not begin from file size alone. It requires:

- an importer inventory;
- model and helper ownership decisions;
- migration compatibility checks;
- stable re-export or migration strategy;
- focused and full-suite validation.

### Agent orchestration

`src/agent_loop.py` coordinates model interaction, tool selection, policy decisions,
multi-round execution, and background behaviour. Extraction work must preserve tool
event semantics, policy enforcement, cancellation, and test patch points.

Historical agent-loop modularization discussion is tracked in
[#3266](https://github.com/odysseus-dev/odysseus/issues/3266).

### Tool implementation boundaries

Tool implementation is no longer represented by one proposed future package alone.
Current responsibilities are distributed across:

- `src/tool_execution.py`;
- `src/tool_schemas.py`;
- `src/tool_index.py`;
- `src/tool_policy.py`;
- `src/tool_security.py`;
- `src/agent_tools/`;
- `src/tools/`;
- remaining compatibility surfaces such as `src/tool_implementations.py`.

Historical tool modularization work is tracked in
[#3629](https://github.com/odysseus-dev/odysseus/issues/3629).

### Route ownership

`routes/` now contains both flat modules and domain packages. Existing package
boundaries should be extended only through focused changes. Broad mechanical route
movement would affect registration, imports, tests, monkeypatch targets, and
compatibility paths.

### Frontend concentration

The no-build frontend contains several large JavaScript modules and one central CSS
file. Refactors should preserve module load order, global compatibility exports,
DOM contracts, deep-link handling, and browser behaviour.

## Non-implemented architecture options

> [!NOTE]
> The paths below are historical or possible design directions. They do not describe
> the current repository and are not approved implementation plans.

Earlier planning discussed:

- renaming `app.py` to `main.py`;
- moving agent orchestration into a new `src/agent/` package;
- introducing broad `src/domain/`, `src/infra/`, `src/api/`, or `src/pkg/` layers;
- moving all routes into domain subpackages;
- splitting database models into a new infrastructure hierarchy.

These options should be reconsidered against the current tree rather than copied
forward as assumed targets.

## Refactor guardrails

- Keep structural changes behaviour-preserving.
- Change one ownership boundary at a time.
- Do not mix file movement with unrelated feature work.
- Preserve existing import and monkeypatch paths where compatibility is required.
- Identify focused tests before modifying high-authority modules.
- Validate startup, imports, and affected runtime paths.
- Avoid repository-wide package reorganizations without maintainer agreement.
- Treat generated metrics as snapshots, not architectural decisions.

## Reproduce the snapshot

Run these commands from the repository root.

```bash
# Tracked directory totals
for dir in src routes core services mcp_servers scripts static/js tests; do
  files="$(git ls-files "$dir" | wc -l)"
  python_files="$(git ls-files "$dir" '*.py' | wc -l)"

  printf '%-14s tracked=%-5s python=%-5s\n' \
    "$dir" \
    "$files" \
    "$python_files"
done

# Largest tracked backend files
git ls-files \
  'app.py' \
  'launcher.py' \
  'setup.py' \
  'core/*.py' \
  'core/**/*.py' \
  'routes/*.py' \
  'routes/**/*.py' \
  'services/*.py' \
  'services/**/*.py' \
  'src/*.py' \
  'src/**/*.py' \
  'mcp_servers/*.py' \
  'scripts/*.py' \
  'scripts/**/*.py' |
xargs wc -l |
sort -nr |
head -31

# Largest tracked frontend source files
git ls-files \
  'static/*.js' \
  'static/*.css' \
  'static/*.html' \
  'static/**/*.js' \
  'static/**/*.css' \
  'static/**/*.html' |
grep -vE '\.min\.js$' |
xargs wc -l |
sort -nr |
head -31
```

## Validation for architecture changes

Use the smallest relevant checks first, then expand according to risk:

```bash
python3 -m compileall -q app.py core routes services src
venv/bin/python -m pytest tests/<focused-test-file>.py -q
venv/bin/python -m pytest -q
```

Startup, browser, Docker, and integration checks may also be required depending on
the affected boundary.

## Related documentation

- [Documentation style](../docs/STYLE.md)
- [Discovery maps](../discovery/README.md)
- [Current system map](../discovery/system-map.md)
- [Safety boundaries](../discovery/safety-boundaries.md)
- [Frontend module summary](../static/js/MODULE_SUMMARY.md)
- [Testing standard](../tests/TESTING_STANDARD.md)
