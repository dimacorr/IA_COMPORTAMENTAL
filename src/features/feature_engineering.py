from typing import List, Dict
import pandas as pd
from src.domain.entities import EnviosCliente

class FeatureEngineering:
    COLUMNS = [
        "hour", "weekday", "total_sent_agg", "response_rate",
        "mean_delay", "unusual_response_rate", "unusual_mean_delay", "status"
    ]

    @staticmethod
    def compute_features(envios: List[EnviosCliente]) -> pd.DataFrame:
        if not envios:
            return pd.DataFrame(columns=FeatureEngineering.COLUMNS)

        rows = []
        for e in envios:
            sent_at = pd.to_datetime(e.sent_at)
            response_at = pd.to_datetime(e.response_at) if e.response_at else None
            response_time = (response_at - sent_at).total_seconds() if response_at else 0.0

            rows.append({
                "client_id": e.client_id,
                "transaction_id": e.envio_id,
                "hour": sent_at.hour,
                "weekday": sent_at.weekday(),
                "total_sent": 1,
                "response_rate": 1 if response_at else 0,
                "mean_delay": response_time,
                "status": getattr(e.transaction, "status", "approved"),
            })

        df = pd.DataFrame(rows)

        # Agregación por cliente
        agg = df.groupby("client_id").agg(
            total_sent=("total_sent", "sum"),
            response_rate=("response_rate", "mean"),
            mean_delay=("mean_delay", "mean"),
        ).reset_index()

        df = df.merge(agg, on="client_id", suffixes=("", "_agg"))

        # Flags heurísticos
        df["unusual_response_rate"] = (
            df["response_rate_agg"] < df["response_rate_agg"].mean() * 0.5
        ).astype(int)
        df["unusual_mean_delay"] = (
            df["mean_delay_agg"] > df["mean_delay_agg"].mean() * 2
        ).astype(int)

        # Normalizamos columnas finales
        df["response_rate"] = df["response_rate_agg"]
        df["mean_delay"] = df["mean_delay_agg"]

        return df[FeatureEngineering.COLUMNS]

    @staticmethod
    def compute_features_from_payload(payload: Dict) -> pd.DataFrame:
        ts = payload.get("timestamp") or payload.get("sent_at")
        sent_at = pd.to_datetime(ts) if ts else pd.Timestamp.now()

        row = {
            "hour": sent_at.hour,
            "weekday": sent_at.weekday(),
            "total_sent_agg": int(payload.get("total_sent", 1)),
            "response_rate": float(payload.get("response_rate", 0.0)),
            "mean_delay": float(payload.get("mean_delay", 0.0)),
            "unusual_response_rate": int(payload.get("response_rate", 0.0) < 0.25),
            "unusual_mean_delay": int(payload.get("mean_delay", 0.0) > 120.0),
            "status": payload.get("status", "unknown"),
        }

        return pd.DataFrame([row], columns=FeatureEngineering.COLUMNS)