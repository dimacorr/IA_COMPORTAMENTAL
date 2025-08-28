from abc import ABC, abstractmethod
from typing import Dict, Any

class PredictorService(ABC):
    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recibe un diccionario con las features (payload) y devuelve
        un diccionario con la predicción (prediction, probability, etc).
        """
        raise NotImplementedError
