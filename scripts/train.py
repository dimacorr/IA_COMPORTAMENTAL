from src.infra.repository_postgres import EnviosRepository
from src.usecases.train_model import TrainModelUseCase
from src.infra.models_store import ModelStore


def main():
    print(">>> Iniciando entrenamiento del modelo de fraude/comportamiento")

    # --- Repositorio (infraestructura) ---
    repo = EnviosRepository()
    envios_entities = repo.fetch_as_entities()
    print(f"Datos cargados: {len(envios_entities)} registros")

    # --- Caso de uso ---
    model_store = ModelStore("models")
    trainer = TrainModelUseCase(model_store=model_store)

    metrics = trainer.execute(envios_entities)

    # --- Reporte ---
    print("ROC AUC:", metrics["roc_auc"])
    print("Reporte de clasificación:")
    print(metrics["classification_report"])


if __name__ == "__main__":
    main()