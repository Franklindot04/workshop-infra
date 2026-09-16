from unittest.mock import patch

import httpx
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from services.processor.app import app, parse_collector_status, server_port


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
    monkeypatch.setenv("PORT", "7000")

    assert server_port() == 7000


def test_default_port(monkeypatch) -> None:
    monkeypatch.delenv("PROCESSOR_PORT", raising=False)
    monkeypatch.delenv("PORT", raising=False)

    assert server_port() == 8000


def test_collector_metrics() -> None:
    collector_metrics = (
        "# HELP workshop_collector_up Whether the collector is available.\n"
        "# TYPE workshop_collector_up gauge\n"
        "workshop_collector_up 1\n"
    )

    with patch("services.processor.app.httpx.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.text = collector_metrics

        response = client.get("/collector/metrics")

    assert response.status_code == 200
    assert response.text == collector_metrics
    mock_get.assert_called_once_with(
        "http://localhost:8080/metrics",
        timeout=5.0,
        trust_env=False,
    )


def test_collector_metrics_returns_bad_gateway() -> None:
    with patch(
        "services.processor.app.httpx.get",
        side_effect=httpx.ConnectError("collector unavailable"),
    ):
        response = client.get("/collector/metrics")

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Collector metrics are unavailable",
    }


def test_parse_collector_status() -> None:
    metrics = "workshop_collector_up 1\n"

    assert parse_collector_status(metrics) == 1.0


def test_parse_collector_status_with_labels() -> None:
    metrics = 'workshop_collector_up{environment="development"} 0\n'

    assert parse_collector_status(metrics) == 0.0


def test_parse_collector_status_raises_when_metric_is_missing() -> None:
    with pytest.raises(HTTPException) as error:
        parse_collector_status("# TYPE another_metric gauge\n")

    assert error.value.status_code == 502
    assert error.value.detail == "Collector status metric is unavailable"


def test_collector_status_reports_up() -> None:
    collector_metrics = "workshop_collector_up 1\n"

    with patch("services.processor.app.httpx.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.text = collector_metrics

        response = client.get("/collector/status")

    assert response.status_code == 200
    assert response.json() == {
        "collector": "up",
        "value": 1.0,
    }


def test_collector_status_reports_down() -> None:
    collector_metrics = 'workshop_collector_up{environment="development"} 0\n'

    with patch("services.processor.app.httpx.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.text = collector_metrics

        response = client.get("/collector/status")

    assert response.status_code == 200
    assert response.json() == {
        "collector": "down",
        "value": 0.0,
    }


def test_collector_status_returns_bad_gateway() -> None:
    with patch(
        "services.processor.app.httpx.get",
        side_effect=httpx.ConnectError("collector unavailable"),
    ):
        response = client.get("/collector/status")

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Collector metrics are unavailable",
    }
