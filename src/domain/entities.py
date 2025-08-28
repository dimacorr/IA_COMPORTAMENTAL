from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaccion:
    transaction_id: str
    client_id: str
    amount: float
    status: str  # "approved", "alert", "declined"
    timestamp: datetime

@dataclass
class EnviosCliente:
    envio_id: str
    client_id: str
    sent_at: datetime
    response_at: datetime | None = None
    response_class: str | None = None
    transaction: Transaccion | None = None