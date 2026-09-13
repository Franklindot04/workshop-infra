import os

from fastapi import FastAPI

app = FastAPI(title="workshop-infra processor")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def server_port() -> int:
    port = os.getenv("PROCESSOR_PORT") or os.getenv("PORT") or "8000"
    return int(port)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=server_port())