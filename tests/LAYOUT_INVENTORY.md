# Test layout inventory

> [!NOTE]
> This document is a completed implementation snapshot for the first low-risk
> test-directory reorganization. It does not propose additional file moves and
> is not the canonical definition of the current test taxonomy.

- **Original inventory:** #3712
- **Parent tracker:** #2523
- **Implemented by:** #3842
- **Status:** completed historical snapshot

- **Durable testing policy:** [`TESTING_STANDARD.md`](./TESTING_STANDARD.md)
- **Current testing mechanics:** [`README.md`](./README.md)

## Disposition

This document is retained as a non-canonical historical record of the completed
CLI test relocation.

Reusable testing rules are maintained in `TESTING_STANDARD.md`; current helper,
taxonomy-runner, and execution mechanics are maintained in `README.md`, the test
suite, and its supporting code.

Counts, residual-file observations, and path listings in this document are
snapshot evidence only. They must not be maintained as durable repository truth.

Any additional test relocation requires a separately approved issue or work item.

## Purpose

This document preserves the reasoning, scope, and validation contract for the
first mechanical reorganization of the formerly flat `tests/` directory.

The original change moved 28 tests classified as `area_cli` into `tests/cli/`
without changing their assertions, helpers, taxonomy, or runtime behaviour.

Current testing guidance and classification rules are maintained in:

- [`README.md`](./README.md)
- [`TESTING_STANDARD.md`](./TESTING_STANDARD.md)
- [`_taxonomy.py`](./_taxonomy.py)

The current repository and test suite remain authoritative when this snapshot
and the implementation differ.

## Why CLI tests were selected

The CLI and script tests were selected as the first low-risk group because they
formed a narrow, mechanically identifiable boundary:

- script entry points were loaded through shared CLI helpers;
- database access used controlled stubs rather than persistent sessions;
- the tests did not require FastAPI application or route setup;
- the tests did not require a real database;
- taxonomy classification could be derived consistently from filenames;
- absolute helper imports remained valid after relocation.

This reduced the risk relative to route, security, session, provider, and
heterogeneous unit-test groups.

## Completed implementation

Repository history records the implementation as:

- `83af3ca test: move area_cli tests into cli directory (#3842)`

The following 28 files were included in that completed move:

- `tests/cli/test_calendar_cli_name.py`
- `tests/cli/test_contacts_cli_rows.py`
- `tests/cli/test_cookbook_cli_state.py`
- `tests/cli/test_docs_cli_content_length.py`
- `tests/cli/test_gallery_cli_album_count.py`
- `tests/cli/test_gallery_cli_preview.py`
- `tests/cli/test_logs_cli_resolve_nonstring.py`
- `tests/cli/test_mail_cli_read_empty_fetch.py`
- `tests/cli/test_mail_cli_recipients.py`
- `tests/cli/test_mcp_cli_env_serialize.py`
- `tests/cli/test_mcp_cli_json.py`
- `tests/cli/test_memory_cli_rows.py`
- `tests/cli/test_notes_cli_items.py`
- `tests/cli/test_personal_cli_rows.py`
- `tests/cli/test_preset_cli_invalid_entries.py`
- `tests/cli/test_preset_cli_set_corrupt_entry.py`
- `tests/cli/test_preset_cli_store.py`
- `tests/cli/test_research_cli_preview.py`
- `tests/cli/test_research_cli_status.py`
- `tests/cli/test_research_cli_status_filter.py`
- `tests/cli/test_research_cli_store.py`
- `tests/cli/test_sessions_cli.py`
- `tests/cli/test_signature_cli_export.py`
- `tests/cli/test_skills_cli_preview.py`
- `tests/cli/test_skills_cli_rows.py`
- `tests/cli/test_tasks_cli_preview.py`
- `tests/cli/test_theme_cli_store.py`
- `tests/cli/test_webhook_cli_mask.py`

## Original exclusions

The original inventory deliberately excluded:

- `tests/test_backup_cli_security.py`, because its security classification
  outranked the CLI token in its filename;
- taxonomy and focused-runner infrastructure, including
  `tests/test_taxonomy.py` and `tests/test_run_focus.py`;
- script-oriented tests not classified as `area_cli`;
- route, service, security, session, JavaScript, helper, and broad unit-test
  groups.

These exclusions kept the implementation mechanical and prevented it from
mixing taxonomy changes, assertion changes, helper extraction, or unrelated
test-suite restructuring.

## Current repository observation

The current taxonomy classifies 30 files as `area_cli`:

| Location | Files |
|---|---:|
| `tests/cli/` | 28 |
| Flat `tests/` directory | 2 |

The two currently classified CLI tests outside `tests/cli/` are:

- `tests/test_calendar_cli_overlap.py`
- `tests/test_memory_cli_add_nondict.py`

These files were not part of the original 28-file implementation.

Their presence is recorded solely to keep this snapshot accurate. This
documentation update does not recommend moving them, changing their taxonomy,
or opening implementation work. Any future test-layout change requires separate
maintainer agreement, scope, and validation.

## Validation contract preserved by the original move

The completed implementation was designed to preserve:

- identical `area_cli` selection before and after relocation;
- successful direct execution of the relocated tests;
- successful whole-suite collection;
- unchanged taxonomy and focused-runner behaviour;
- no stale references to the former flat paths;
- no production-code changes.

Relevant current verification commands include:

```bash
venv/bin/python tests/run_focus.py --dry-run --area cli
venv/bin/python -m pytest -m area_cli -q
venv/bin/python -m pytest tests/cli/ -q
venv/bin/python -m pytest tests/test_taxonomy.py tests/test_run_focus.py -q
venv/bin/python -m pytest --collect-only -q
```

These commands describe validation coverage. This snapshot does not claim that
they were executed as part of the present documentation update.

## Non-goals

This document does not:

- propose moving or renaming tests;
- redefine taxonomy classifications;
- change test behaviour or assertions;
- prescribe the next test-suite refactor;
- replace the testing standard;
- create implementation work from the two current residual files.
