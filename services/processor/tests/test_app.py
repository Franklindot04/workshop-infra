from services.processor.app import app, server_port
from fastapi.testclient import TestClient


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_processor_port_takes_priority(monkeypatch) -> None:
    monkeypatch.setenv("PROCESSOR_PORT", "9000")
    monkeypatch.setenv("PORT", "7000")

    assert server_port() == 9000


def test_port_is_used_as_fallback(monkeypatch) -> None:
    monkeypatch.delenv("PROCESSOR_PORT", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.setenv("PORT", "7000")

    assert server_port() == 7000


def test_default_port(monkeypatch) -> None:
    monkeypatch.delenv("PROCESSOR_PORT", raising=False)
    monkeypatch.delenv("PORT", raising=False)

    assert server_port() == 8000