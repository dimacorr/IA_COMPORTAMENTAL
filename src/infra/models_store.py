import joblib
import logging
from pathlib import Path
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class ModelStore:

    def __init__(self, base_dir: Optional[str] = None) -> None:
        """
        Inicializa el almacenamiento del modelo.

        Args:
            base_dir (Optional[str]): Ruta base donde se guardarán los modelos.
                                      Si no se indica, se usa la raíz del proyecto con /models.
        """
        # Determinar carpeta base del proyecto
        project_root = Path(__file__).resolve().parents[2]
        self.base_dir = Path(base_dir) if base_dir else project_root / "models"

        # Paths de archivos
        self.model_path: Path = self.base_dir / "model.pkl"
        self.features_path: Path = self.base_dir / "features.pkl"

        # Cache en memoria
        self._model: Optional[Any] = None
        self._features: Optional[List[str]] = None

        # Crear carpeta si no existe
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load_model(self) -> Any:
        """
        Carga el modelo entrenado desde disco (singleton).

        Returns:
            Any: El modelo cargado en memoria.

        Raises:
            FileNotFoundError: Si no existe el archivo model.pkl.
        """
        if self._model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(f"No se encontró modelo en {self.model_path}")
            logger.info(f"Cargando modelo desde: {self.model_path}")
            self._model = joblib.load(self.model_path)
            logger.info("Modelo cargado exitosamente")
        return self._model

    def load_features(self) -> List[str]:
        """
        Carga la lista de columnas usadas en el entrenamiento.

        Returns:
            List[str]: Lista de nombres de features.

        Raises:
            FileNotFoundError: Si no existe el archivo features.pkl.
        """
        if self._features is None:
            if not self.features_path.exists():
                raise FileNotFoundError(f"No se encontraron features en {self.features_path}")
            logger.info(f"Cargando features desde: {self.features_path}")
            self._features = joblib.load(self.features_path)
        return self._features

    def save_model(self, model: Any, features: List[str]) -> None:
        """
        Guarda el modelo y las columnas de features en disco.

        Args:
            model (Any): Modelo de ML a guardar.
            features (List[str]): Lista de features usadas en entrenamiento.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self.model_path)
        joblib.dump(features, self.features_path)
        logger.info(f"Modelo guardado en {self.model_path}")
        logger.info(f"Features guardadas en {self.features_path}")
        self._model = model
        self._features = features


def get_model_dir(base_dir: Optional[str] = None) -> Path:
    """
    Devuelve la ruta absoluta a la carpeta /models y la crea si no existe.

    Args:
        base_dir (Optional[str]): Ruta base alternativa.

    Returns:
        Path: Ruta de la carpeta de modelos.
    """
    project_root = Path(__file__).resolve().parents[2]
    path = Path(base_dir) if base_dir else project_root / "models"
    path.mkdir(parents=True, exist_ok=True)
    return path
