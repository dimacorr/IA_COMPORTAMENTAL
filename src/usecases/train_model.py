from typing import List, Dict, Any
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
from pathlib import Path
import joblib

from src.domain.entities import EnviosCliente
from src.features.feature_engineering import FeatureEngineering
from src.infra.models_store import ModelStore


class TrainModelUseCase:
    """
    Caso de uso para entrenar un modelo de clasificación de fraude/comportamiento.
    Orquesta: extracción de features, entrenamiento, evaluación y persistencia.
    """

    def __init__(
        self,
        model_store: ModelStore,
        n_estimators: int = 200,
        random_state: int = 42,
        test_size: float = 0.2,
    ):
        self.model_store = model_store
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.test_size = test_size

    def execute(self, envios: List[EnviosCliente]) -> Dict[str, Any]:
        if not envios:
            raise ValueError("No hay envíos para entrenar el modelo.")

        # --- Feature engineering ---
        features_df = FeatureEngineering.compute_features(envios)
        feature_columns = [
            "hour", "weekday", "total_sent_agg",
            "response_rate", "mean_delay",
            "unusual_response_rate", "unusual_mean_delay"
        ]
        X = features_df[feature_columns]
        y = features_df["status"].apply(lambda s: 1 if s in ["alert", "declined"] else 0)

        # --- División train/test ---
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        # --- Entrenamiento ---
        clf = RandomForestClassifier(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )
        clf.fit(X_train, y_train)

        # --- Evaluación ---
        preds_proba = clf.predict_proba(X_test)[:, 1]
        preds = clf.predict(X_test)
        metrics = {
            "roc_auc": float(roc_auc_score(y_test, preds_proba)),
            "classification_report": classification_report(y_test, preds, output_dict=True),
        }

        # --- Persistencia ---
        self.model_store.save_model(clf, feature_columns)

        return metrics