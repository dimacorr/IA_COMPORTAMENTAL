from typing import Any, Dict
from src.domain.behavior import BehaviorFlags, Probability
from src.domain.services import PredictorService

class PredictResponseUseCase:
    """
       UseCase para procesar la predicción de fraude.
       Evalúa tanto la probabilidad del modelo como los flags de comportamiento
       para determinar si la transacción es fraude o no.
       """

    def __init__(self, predictor: PredictorService, threshold: float) -> None:
        self.predictor = predictor
        self.threshold = threshold

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Behavior flags
        behavior_flags = BehaviorFlags(
            unusual_response_rate=payload.get("response_rate", 1.0) < 0.25,
            unusual_mean_delay=payload.get("mean_delay", 0) > 120.0,
        )

        # Inferencia
        result = self.predictor.predict(payload)
        probability = Probability(result["probability"])

        is_fraud = (
                probability.is_fraud(self.threshold) or
                behavior_flags.unusual_response_rate or
                behavior_flags.unusual_mean_delay
        )

        result["prediction"] = "fraude" if is_fraud else "no_fraude"
        result["threshold_used"] = self.threshold

        # Adjuntar flags de comportamiento al resultado
        result["behavior_flags"] = {
            "unusual_response_rate": behavior_flags.unusual_response_rate,
            "unusual_mean_delay": behavior_flags.unusual_mean_delay,
        }

        return result
