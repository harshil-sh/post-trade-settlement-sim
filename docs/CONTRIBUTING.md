# Contributing

## Goal

Keep the codebase clean, understandable, and production-minded.

## Development principles

- prefer simple and explicit designs
- keep domain logic out of controllers
- write tests for business logic
- document meaningful architectural decisions
- avoid silent magic

## Branching

Suggested:
- `main` for stable state
- short-lived feature branches for changes

## Commit style

Use clear, small commits.

Examples:
- `feat: add idempotent trade submission endpoint`
- `test: add retry policy integration tests`
- `docs: add DLQ replay scenario`

## Pull requests

PRs should include:
- summary of change
- why the change was needed
- testing performed
- docs updated if applicable

## Code review checklist

- does the change preserve idempotency?
- does it improve or harm observability?
- are failure modes handled explicitly?
- are tests added at the right level?
- are docs still accurate?