# Documentation style

This guide defines the shared structure and writing conventions for Odysseus documentation.

## Principles

- Write for a clear audience and purpose.
- State whether a document is canonical, informational, a snapshot, or planning material.
- Prefer current behaviour over historical explanation.
- Link to source files, tests, issues, or other documentation when useful.
- Separate verified behaviour from assumptions, open questions, and future work.
- Keep headings descriptive and consistent.
- Use Markdown callouts where status or risk must be visible.
- Do not use emojis.

## Document status

Use a status callout near the top when the document is not normal canonical guidance.

### Canonical documentation

> [!IMPORTANT]
> This document describes accepted current behaviour. Verify implementation-sensitive details against the current code and tests.

### Discovery material

> [!NOTE]
> This is non-canonical discovery material. It records code-grounded observations and open questions.

### Snapshot or inventory

> [!WARNING]
> This document is a dated snapshot. Counts, paths, and implementation details may drift as the codebase changes.

### Planning material

> [!NOTE]
> This document records planning context. It does not define current runtime behaviour or guarantee future implementation.

## Recommended structure

Use the following sections where relevant:

1. Title
2. Purpose or status callout
3. Scope
4. Current behaviour or guidance
5. Safety, limitations, or known gaps
6. Validation or evidence
7. Related documentation

Not every document needs every section.

## Writing style

- Use concise sentences.
- Prefer direct language.
- Avoid jokes, filler, and informal warnings.
- Avoid repeating the same guidance across several files.
- Link to the owning document instead of duplicating large sections.
- Use lists for procedures, requirements, and comparisons.
- Use tables only when they improve scanning.
- Use fenced code blocks with an appropriate language identifier.
- Use relative repository links for internal files.

## Authority

The current code, tests, and configuration are the source of truth for implemented behaviour.

Canonical documentation describes accepted behaviour and supported workflows.

Discovery, inventory, and planning documents must identify themselves explicitly and must not silently become behavioural specifications.
