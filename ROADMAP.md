# Roadmap

This document provides a high-level view of the areas Odysseus is currently improving.

It is directional rather than exhaustive. Priorities may change as the project evolves, defects are discovered, and maintainers learn more from implementation work and user feedback.

For current implementation work, see the open [GitHub issues](https://github.com/odysseus-dev/odysseus/issues). Accepted behaviour should be documented in the repository alongside the code.

## Current priorities

### Reliability and setup

- Improve fresh-install and smoke-test coverage across supported environments.
- Make provider setup, probing, and failure states more predictable.
- Improve Cookbook reliability across hardware, operating systems, drivers, shells, and serving backends.
- Improve degraded-state reporting and recovery guidance when optional services are unavailable.

### Local model workflows

- Improve hardware-aware model recommendations and compatibility guidance.
- Evaluate serving optimizations, including speculative decoding, through reproducible benchmarks.
- Improve installation, preflight checks, logging, and error reporting for local model serving.
- Reduce prompt and context overhead for smaller local models.

### Safety and resilience

- Continue hardening tool execution, filesystem access, credentials, networking, and destructive operations.
- Treat content from documents, notes, memories, skills, and fetched pages as potentially untrusted.
- Improve security-focused regression coverage and operational guidance.
- Review integrations that expand access to sensitive data or privileged operations.

### Product usability

- Improve first-run setup, onboarding, hints, and tours.
- Improve accessibility, keyboard navigation, focus behaviour, contrast, and reduced-motion support.
- Improve empty states, error messages, and recovery paths.
- Strengthen Notes, Todos, Editor, mobile, and everyday workspace flows.

### Architecture and maintainability

- Reduce duplication and technical debt through focused, reviewable refactors.
- Improve subsystem documentation as behaviour and architecture become stable.
- Remove stale code, obsolete feature flags, and unsupported integrations.
- Keep implementation decisions grounded in current code and verified behaviour.

## Tracking work

Concrete implementation tasks, defects, proposals, and technical investigations are tracked in:

- [GitHub Issues](https://github.com/odysseus-dev/odysseus/issues)
- [Contributing Guide](CONTRIBUTING.md)

Maintainers may use additional private coordination tools for ownership, planning, and unresolved decisions.

This roadmap is not a complete backlog or a guarantee that a particular item will be delivered.
