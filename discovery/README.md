# Odysseus discovery maps

Compact, code-grounded discovery maps of cross-cutting systems in the checked-in Odysseus codebase. They preserve investigation context and open factual questions; they are not canonical subsystem specifications, a feature certification, or a substitute for normal testing.

> [!IMPORTANT]
> Checked-in code is the source of truth for current behaviour. Mature subsystem specifications, where they exist, are the canonical documentation of accepted subsystem behaviour. Check code, tests, and configuration before reconciling a discovery finding. Discovery remains non-canonical.

## Explore the maps

| Document | Purpose |
|---|---|
| [Current system map](system-map.md) | Records evidence locations, confirmed local observations, and factual open questions about subsystem boundaries. |
| [Safety boundaries](safety-boundaries.md) | Records evidence about broad authority, safeguards, confirmed risks or gaps, and unverified behaviour. |

## Working rules

- **Trace the code first.** Confirm the current path in source before recording a claim.
- **Promote selectively.** When an owning mature specification exists, add a fact only when it is verified, useful, and not already represented there.
- **Record missing ownership.** When no owning specification exists, retain the verified finding in discovery and record missing documentation ownership as a follow-up.
- **Retain uncertainty here.** Keep unresolved questions and useful investigation context in discovery rather than treating them as canonical truth.
- **Keep specifications current-state only.** Do not record intentions, design direction, refactor plans, decision history, priority, ownership, or sequencing here.
- **Investigate with cause.** Do not exhaustively revalidate existing functionality without a report, visible failure, relevant change, or high-authority review need.
- **Review authority carefully.** Give execution, data access, external tools, credentials, destructive operations, and unattended work focused review.
- **Use stable locations.** Cite modules, routes, classes, and functions instead of fragile line ranges or generated evidence tables.

## Reconciliation flow

1. Start with the relevant map and trace the cited code.
2. Classify the finding against current source evidence and an owning mature specification where one exists.
3. Promote only verified, useful facts that are missing from an existing owning specification.
4. When no owning specification exists, retain the verified finding here and record missing documentation ownership as a follow-up; otherwise retain unresolved context here and correct stale wording.

> [!NOTE]
> This package intentionally contains no generator, validator, maturity scale, feature database, or parallel work tracker. The [architecture runtime inventory](./architecture-runtime-inventory.md) preserves dated structural metrics, investigation context, and historical planning as an explicitly non-canonical snapshot.
