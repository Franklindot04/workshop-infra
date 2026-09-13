# Service Configuration Conventions

This document defines initial configuration conventions for workshop-infra services. It applies to both Go and Python services.

## Environment variables

- Use `UPPER_SNAKE_CASE` for all environment variable names.
- Prefix service-specific variables with the service name, e.g. `COLLECTOR_PORT`, `PROCESSOR_PORT`.
- Use `PORT` as a generic override when deploying in containers.
- Read environment variables at startup; do not change behavior based on config files checked into source control.

## Default ports

- Collector (Go): `8080`
- Processor (Python): `8000`

Local development should use these defaults unless overridden by `PORT`.

## Local development configuration

- Use `.env` files for local overrides only; never commit `.env`.
- Commit `.env.example` with placeholder values and documentation.
- Validate required variables at service startup and fail fast if missing.

## Required versus optional settings

- **Required**: Variables without which the service cannot start (e.g. `PORT` if not using a default).
- **Optional**: Variables with sensible defaults or used only for optional features.

Document all required variables in each service's README.

## Secrets

- Never commit secrets to source control.
- Store secrets in environment variables or a secrets manager.
- Use `.env.example` to document required secret names without values.
- Rotate secrets if they are ever exposed in logs or commits.

## Naming conventions

- Service name: lowercase, hyphen-separated (e.g. `collector`, `processor`).
- Environment variable prefix: uppercase, same as service name (e.g. `COLLECTOR_`, `PROCESSOR_`).
- Configuration keys in code: match environment variable names or use clear, consistent mappings.

These conventions keep configuration consistent across Go and Python services and simplify future deployment and automation.
