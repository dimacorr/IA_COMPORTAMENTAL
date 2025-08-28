import os
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    """Configuración central del proyecto."""

    def __init__(self, env_file: str = ".env"):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent

        # Cargar .env
        env_path = self.BASE_DIR / env_file
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Cargado .env desde: {env_path}")
        else:
            print(f"Archivo {env_file} no encontrado en {self.BASE_DIR}")

        # Variables requeridas
        self.DATABASE_URL: str = self._get_env("DATABASE_URL", required=True)

        # Opcionales
        self.MODEL_PATH: Path = Path(self._get_env("MODEL_PATH", "models/model.pkl"))
        self.MODEL_DIR: Path = self.MODEL_PATH.parent
        self.THRESHOLD: float = self._get_float_env("THRESHOLD", 0.7)

    def _get_env(self, key: str, default=None, required: bool = False) -> str:
        value = os.getenv(key, default)
        if required and not value:
            raise ValueError(f"La variable de entorno '{key}' es obligatoria y no está definida.")
        return value

    def _get_float_env(self, key: str, default: float) -> float:
        value_str = os.getenv(key)
        if value_str is None:
            return default
        try:
            return float(value_str)
        except ValueError:
            return default

# Instancia global
settings = Settings()
print(f"THRESHOLD configurado: {settings.THRESHOLD}")
print(f"MODEL_PATH configurado: {settings.MODEL_PATH}")