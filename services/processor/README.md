# Processor Service

Initial Python service for processing operational data within workshop-infra.

## Run locally

From the repository root:

```bash
python -m pip install -r services/processor/requirements.txt
python services/processor/app.py
```

The service listens on port `8000` by default.

## Configuration

The service uses the following port precedence:

1. `PROCESSOR_PORT`
2. `PORT`
3. `8000` by default

The preferred variable is `PROCESSOR_PORT`. The generic `PORT` variable is supported as a compatibility fallback.

The collector endpoint is configured through `COLLECTOR_URL`. It defaults to:

```text
http://localhost:8080
```

When running through Docker Compose, the processor uses:

```text
http://collector:8080
```

## Health and readiness

### Health check

The health endpoint confirms that the processor service is running.

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### Readiness check

The readiness endpoint confirms that the processor can reach the collector metrics endpoint.

```bash
curl -i http://localhost:8000/ready
```

When the collector is reachable, the processor returns:

```json
{"status":"ready"}
```

If the collector metrics endpoint is unavailable, the processor returns `503 Service Unavailable`:

```json
{"detail":"Collector metrics are unavailable"}
```

## Collector endpoints

### Proxy collector metrics

The processor exposes the collector’s Prometheus metrics through:

```bash
curl -i http://localhost:8000/collector/metrics
```

The endpoint returns the collector metrics as plain text.

### Collector status

The processor exposes the collector’s current status through:

```bash
curl -i http://localhost:8000/collector/status
```

Example response when the collector is available:

```json
{
  "collector": "up",
  "value": 1.0
}
```

Example response when the collector reports that it is unavailable:

```json
{
  "collector": "down",
  "value": 0.0
}
```

If the processor cannot reach the collector metrics endpoint, it returns `502 Bad Gateway`.

## API documentation

Open `http://localhost:8000/docs` in a browser.

## Tests

```bash
PYTHONPATH=. pytest services/processor/tests
```
