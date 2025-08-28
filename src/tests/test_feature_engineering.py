import pandas as pd
import pytest
from src.features.feature_engineering import compute_features, compute_features_from_payload


class DummyTransaction:
    def __init__(self, status="approved"):
        self.status = status


class DummyEnvio:
    def __init__(self, client_id, envio_id, sent_at, response_at=None, status="approved"):
        self.client_id = client_id
        self.envio_id = envio_id
        self.sent_at = sent_at
        self.response_at = response_at
        self.transaction = DummyTransaction(status)


def test_empty_list_returns_empty_df():
    out = compute_features([])
    # Debe devolver DataFrame vacío con columnas consistentes
    assert out.empty
    expected_cols = ["hour", "weekday", "total_sent_agg", "response_rate",
                     "mean_delay", "unusual_response_rate", "unusual_mean_delay", "status"]
    assert list(out.columns) == expected_cols


def test_single_envio_with_response():
    envio = DummyEnvio(
        client_id="c1",
        envio_id="t1",
        sent_at="2025-01-01T00:00:00",
        response_at="2025-01-01T00:05:00",
        status="approved"
    )
    out = compute_features([envio])
    assert not out.empty
    # La hora debe ser 0
    assert out["hour"].iloc[0] == 0
    # Debe detectar respuesta
    assert out["response_rate"].iloc[0] == 1.0
    # Mean delay debe ser 300 segundos (5 minutos)
    assert out["mean_delay"].iloc[0] == 300.0
    # Status debe estar presente
    assert out["status"].iloc[0] == "approved"


def test_multiple_envios_same_client():
    envios = [
        DummyEnvio("c1", "t1", "2025-01-01T10:00:00", "2025-01-01T10:01:00"),
        DummyEnvio("c1", "t2", "2025-01-01T11:00:00", None)  # sin respuesta
    ]
    out = compute_features(envios)
    assert out["total_sent_agg"].iloc[0] == 2
    assert 0 <= out["response_rate"].iloc[0] <= 1
    assert "unusual_response_rate" in out.columns


def test_compute_features_from_payload():
    payload = {
        "timestamp": "2025-01-01T15:00:00",
        "total_sent": 5,
        "response_rate": 0.7,
        "mean_delay": 60,
        "status": "approved"
    }
    out = compute_features_from_payload(payload)
    assert out.shape[0] == 1
    assert out["hour"].iloc[0] == 15
    assert out["weekday"].iloc[0] == 2  # 2025-01-01 es miércoles
    assert out["unusual_response_rate"].iloc[0] == 0
    assert out["unusual_mean_delay"].iloc[0] == 0
