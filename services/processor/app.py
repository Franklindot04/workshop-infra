import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(title="workshop-infra processor")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/collector/metrics", response_class=PlainTextResponse)
def collector_metrics() -> str:
    collector_url = os.getenv("COLLECTOR_URL", "http://localhost:8080").rstrip("/")

    try:
        response = httpx.get(
            f"{collector_url}/metrics",
            timeout=5.0,
            trust_env=False,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Collector metrics are unavailable",
        ) from exc

    return response.text


def server_port() -> int:
    port = os.getenv("PROCESSOR_PORT") or os.getenv("PORT") or "8000"
    return int(port)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=server_port())
