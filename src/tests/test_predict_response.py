import pytest
from src.usecases.predict_response import PredictResponseUseCase
from src.domain.services import PredictorService


class FakePredictor(PredictorService):
    def predict(self, payload):
        return {
            "prediction": "NO_FRAUDE",
            "probabilities": {"no_fraude": 0.9, "fraude": 0.1},
        }


def test_predict_response_usecase_with_normal_behavior():
    predictor = FakePredictor()
    use_case = PredictResponseUseCase(predictor)

    payload = {
        "client_id": "201",
        "amount": 50000.00,
        "response_rate": 0.7,
        "mean_delay": 30
    }

    result = use_case.execute(payload)

    assert result["prediction"] == "NO_FRAUDE"
    assert result["probabilities"]["no_fraude"] == 0.9
    assert result["behavior_flags"]["unusual_response_rate"] is False
    assert result["behavior_flags"]["unusual_mean_delay"] is False


def test_predict_response_usecase_with_unusual_behavior():
    predictor = FakePredictor()
    use_case = PredictResponseUseCase(predictor)

    payload = {
        "client_id": "201",
        "amount": 50000.00,
        "response_rate": 0.1,   # Muy bajo
        "mean_delay": 200       # Muy alto
    }

    result = use_case.execute(payload)

    assert result["prediction"] == "NO_FRAUDE"
    assert result["behavior_flags"]["unusual_response_rate"] is True
    assert result["behavior_flags"]["unusual_mean_delay"] is True
