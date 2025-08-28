from sqlalchemy import create_engine, text
from typing import List
from src.domain.entities import EnviosCliente, Transaccion
from src.infra.config import Settings

class EnviosRepository:
    def __init__(self, engine=None):
        if engine:
            self.engine = engine
        else:
            settings = Settings()
            if not settings.DATABASE_URL:
                raise RuntimeError("DATABASE_URL no configurada")
            self.engine = create_engine(settings.DATABASE_URL)

    def fetch_as_entities(self) -> List[EnviosCliente]:
        query = text("""
            SELECT e.client_id,
                   e.transaction_id,
                   e.sent_at,
                   e.response_at,
                   e.response_class,
                   t.amount,
                   t.status,
                   t.timestamp AS trx_timestamp
            FROM envios_cliente e
            LEFT JOIN transacciones t ON t.transaction_id = e.transaction_id
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = [dict(row) for row in result.mappings()]

        entidades = []
        for row in rows:
            trans = Transaccion(
                transaction_id=row["transaction_id"],
                client_id=row["client_id"],
                amount=row["amount"] or 0,
                status=row["status"] or "approved",
                timestamp=row["trx_timestamp"]
            )
            entidades.append(
                EnviosCliente(
                    envio_id=row["transaction_id"],
                    client_id=row["client_id"],
                    sent_at=row["sent_at"],
                    response_at=row["response_at"],
                    response_class=row["response_class"],
                    transaction=trans
                )
            )
        return entidades