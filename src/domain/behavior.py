from dataclasses import dataclass

@dataclass(frozen=True)
class BehaviorFlags:
    """
    Value Object que representa indicadores de comportamiento
    relacionados con la respuesta del cliente.
    """
    unusual_response_rate: bool
    unusual_mean_delay: bool


@dataclass(frozen=True)
class Probability:
    """
    Value Object que encapsula una probabilidad de fraude.
    """
    value: float

    def is_fraud(self, threshold: float) -> bool:
        """
        Evalúa si la probabilidad es suficiente para considerar fraude.
        """
        return self.value >= threshold