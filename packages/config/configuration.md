# Service Configuration

Shared configuration conventions for workshop-infra services.

## Environment variable naming

Service-specific configuration variables should use a clear service prefix:

- `COLLECTOR_PORT`
- `PROCESSOR_PORT`

Generic variables such as `PORT` may be supported as compatibility fallbacks where appropriate.

## Port precedence

Services should resolve their listening port in this order:

1. Service-specific port variable.
2. Generic `PORT` fallback.
3. Documented service default.

The service-specific variable should be used in local Compose configuration and normal development workflows.

## Local environment

Use the root `.env.example` as the reference for local configuration.

Local `.env` files may contain environment-specific values and must not be committed.

## Secrets

Secrets must not be committed to the repository. Use environment variables or an appropriate secret-management mechanism for runtime secret values.

## Exceptions

A service may use different configuration conventions when required by its runtime or deployment environment. Such exceptions should be documented in the service README.
