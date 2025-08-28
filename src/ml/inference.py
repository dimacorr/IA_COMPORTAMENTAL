import os
import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
from typing import Dict, Any
from src.domain.services import PredictorService
from src.features.feature_engineering import FeatureEngineering


class FraudPredictor(PredictorService):
    def __init__(self, model_dir: str = None):
        base_dir = model_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models"))
        self.model_path = os.path.join(base_dir, "model.pkl")
        self.features_path = os.path.join(base_dir, "features.pkl")

        self.model = joblib.load(self.model_path)
        if os.path.exists(self.features_path):
            self.feature_columns = joblib.load(self.features_path)
        else:
            self.feature_columns = FeatureEngineering.COLUMNS

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        df = FeatureEngineering.compute_features_from_payload(features)
        X = df.reindex(columns=self.feature_columns).fillna(0)
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0.0).astype(float)
        X_arr = X.values

        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X_arr)[0]
            proba_fraude = float(proba[1]) if len(proba) > 1 else float(proba[0])
            pred_label = int(proba_fraude >= 0.5)  # predicción inicial, luego se ajusta en usecase
        else:
            pred_label = int(self.model.predict(X_arr)[0])
            proba_fraude = None

        label_map = {0: "no_fraude", 1: "fraude"}

        return {
            "prediction": label_map.get(pred_label, "desconocido"),
            "probability": round(proba_fraude, 2) if proba_fraude is not None else 0.0,
        }
