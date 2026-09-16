import os
import re

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(title="workshop-infra processor")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def collector_url() -> str:
    return os.getenv("COLLECTOR_URL", "http://localhost:8080").rstrip("/")


def fetch_collector_metrics() -> str:
    try:
        response = httpx.get(
            f"{collector_url()}/metrics",
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


@app.get("/collector/metrics", response_class=PlainTextResponse)
def collector_metrics() -> str:
    return fetch_collector_metrics()


def parse_collector_status(metrics: str) -> float:
    match = re.search(
        r"^workshop_collector_up(?:\{[^}]*\})?\s+([0-9]+(?:\.[0-9]+)?)\s*$",
        metrics,
        re.MULTILINE,
    )

    if match is None:
        raise HTTPException(
            status_code=502,
            detail="Collector status metric is unavailable",
        )

    return float(match.group(1))


@app.get("/collector/status")
def collector_status() -> dict[str, float | str]:
    value = parse_collector_status(fetch_collector_metrics())

    return {
        "collector": "up" if value == 1 else "down",
        "value": value,
    }


def server_port() -> int:
    port = os.getenv("PROCESSOR_PORT") or os.getenv("PORT") or "8000"
    return int(port)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=server_port())
