from pydantic import BaseModel
from typing import Optional, Dict

# --- Entrada ---
class PredictRequestDTO(BaseModel):
    client_id: str
    amount: float
    tipo_transaccion: str
    channel_code: str
    motor_monitoreo_map: str
    alert_type: str
    dia_semana: int
    client_mobilePhone: str
    response_text: str
    timestamp: str
    total_sent: int
    response_rate: float
    mean_delay: float

# --- Salida ---
class PredictResponseDTO(BaseModel):
    prediction: str
    probability: float
    threshold_used: float
    behavior_flags: Dict[str, bool]