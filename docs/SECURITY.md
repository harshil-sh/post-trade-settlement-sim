# Security

## Scope

This is a portfolio/demo system, but basic secure development practices still apply.

## Principles

- do not commit secrets
- validate all external input
- keep admin endpoints clearly separated
- use least privilege for service access where possible
- sanitize logs to avoid leaking sensitive data

## Secrets

Use environment variables or local secret management.
Never commit:
- database passwords
- broker credentials
- API keys

## Dependencies

- keep dependencies current
- review transitive dependencies periodically
- run vulnerability scanning in CI when possible

## Reporting

For portfolio/demo use, issues can be documented directly in the repository issue tracker or private notes.