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

## Health check

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## API documentation

Open `http://localhost:8000/docs` in a browser.

## Tests

```bash
PYTHONPATH=. pytest services/processor/tests
```
