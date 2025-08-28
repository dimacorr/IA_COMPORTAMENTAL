# Flujo del proyecto de detección de fraude con IA Comportamental

Este proyecto implementa un modelo de Machine Learning que analiza patrones de comportamiento de los clientes frente a 
notificaciones transaccionales, con el fin de identificar posibles fraudes.

---
## 🚀 Flujo General
1. **Carga de datos** 
   * **Fuente:** base de datos Postgres (envios_cliente, transacciones). 
   * Los registros contienen información clave: cliente, transacción, hora de envío, canal utilizado, 
   y respuesta (si existió).
2. **Ingeniería de características (Feature Engineering)**
   * Hora del envío en formato numérico. 
   * Día de la semana de la transacción.
   * Retraso entre el envío y la respuesta.
   * Tasa de respuesta del cliente.
   * Indicadores de comportamiento inusual (ej. respuestas demasiado tardías o ausencia de respuesta).<br>
   👉 Este paso permite que el modelo “entienda” mejor los datos y capture patrones de riesgo.
3. **Entrenamiento del modelo**
   * Algoritmo: RandomForestClassifier balanceado para manejar clases desiguales.
   * Objetivo de clasificación:
     * `1` → Transacción sospechosa (alerta o declinada).
     * `0` → Transacción normal (confirmada o sin problema).
4. **Evaluación del rendimiento**
   * **ROC AUC:** mide la capacidad del modelo para distinguir entre fraude y no fraude.
   * **Reporte de clasificación:** incluye precisión, recall y F1-score.<br>
     👉 Estas métricas permiten validar objetivamente la calidad del modelo.
5. **Persistencia del modelo**
   * Se guarda el modelo entrenado en `models/model.pkl.`
   * Se almacenan las variables usadas (`features.pkl`) para asegurar coherencia entre entrenamiento y predicción.

---
📌 Con este flujo, la solución no solo detecta fraudes, sino que también se adapta al comportamiento real de los clientes, 
creando un enfoque dinámico y robusto para la prevención.

---

## 🛠️ Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes programas:

1. **Python 3.10+** – Para ejecutar scripts y FastAPI.
2. **PostgreSQL** – Base de datos local para almacenar transacciones y registros de clientes.
3. **Git** – Para clonar el repositorio (opcional si ya tienes los archivos).
4. **pip** – Para instalar las dependencias de Python.
5. **psql** – Cliente de línea de comandos para ejecutar el script `schema.sql`.

📌 Nota: Se recomienda usar **Windows, Linux o Mac** y asegurarse de que Python y PostgreSQL estén en el PATH del sistema.

---

## ⚙️ Configuración del entorno
Sigue estos pasos para preparar el proyecto:

1. **Crear entorno virtual** <br>
   Crea y activa un entorno virtual para aislar las dependencias del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac
```

2. **Instalar dependencias** <br>
Con el entorno virtual activo, instala las librerías necesarias:

```powershell
pip install -r requirements.txt
```

3. **Crear base de datos y tablas en PostgreSQL** <br>
Antes de ejecutar el proyecto, asegúrate de tener PostgreSQL corriendo localmente y de crear la base de datos y 
las tablas necesarias. Para facilitar esto, el proyecto incluye un script SQL:

Ejecuta el script `schema.sql` en tu base de datos local antes de correr la aplicación:

```bash
psql -U <usuario> -d <nombre_base_datos> -f sql/schema.sql
```
📌 **Nota:**
* El usuario debe tener permisos para crear bases y tablas.
* DATABASE_URL en `.env` debe apuntar a esta base de datos.

4. **Variables de entorno** <br>
Crea `.env `en la raíz del proyecto:

```powershell
DATABASE_URL=postgresql://user:password@host:port/db
MODEL_DIR=models
THRESHOLD=0.7
```
📌 **Notas:** <br>
DATABASE_URL → Cadena de conexión a PostgreSQL. <br>
MODEL_DIR → Ruta donde se almacenará el modelo entrenado. <br>
THRESHOLD → Umbral de decisión para clasificar fraude/no fraude. <br>

4. **(Opcional) Configurar PYTHONPATH**  <br>
Si aparece el error: 
```bash
ModuleNotFoundError: No module named 'scripts'
```
Configura la variable de entorno `PYTHONPATH` apuntando a la raíz del proyecto.

---
## 🚀 Entrenamiento del modelo

```powershell
python -m scripts.train
```
📌 **Notas:** Solo es necesario si cambias el THRESHOLD o los datos de entrenamiento.

---
## 🚀 Ejecución de la aplicación

```powershell
uvicorn main:app --reload --log-level debug
```
Accede al endpoint a la aplicación:

`POST http://127.0.0.1:8000/predict`

---
## 📦 Estructura del proyecto

```powershell
ia_comportamental/
├── README.md
├── requirements.txt
├── .env
├── main.py                # Entrypoint FastAPI
├── models/
│   ├── model.pkl
│   └── features.pkl
├── scripts/
│   └── train.py           # Script para entrenar
├── sql/
│   └── schema.sql
└── src/
    ├── domain/
    │   ├── entities.py
    │   ├── behavior.py
    │   └── services.py    # Interfaces como PredictorService
    ├── usecases/
    │   ├── train_model.py
    │   ├── schemas.py
    │   └── predict_response.py
    ├── infra/
    │   ├── config.py
    │   ├── repository_postgres.py
    │   └── models_store.py
    ├── features/
    │   └── feature_engineering.py  # FeatureEngineering
    ├── ml/
    │   └── inference.py
    ├── entrypoints/
    │   └── api.py
    └── tests/
        ├── test_feature_engineering.py
        └── test_predict_response.py
```
---
## 🧪 Ejemplo de inferencia

Payload de prueba (No Fraude):
```powershell
{
  "client_id": "302",
  "amount": 1000.00,
  "tipo_transaccion": "compra",
  "channel_code": "WEB",
  "motor_monitoreo_map": "normal",
  "alert_type": "compra_estandar",
  "dia_semana": 2,
  "client_mobilePhone": "3202222222",
  "response_text": "Sí",
  "timestamp": "2025-08-25T10:00:00",
  "total_sent": 1,
  "response_rate": 1.0,
  "mean_delay": 0
}
```

Respuesta esperada:
```powershell
{
    "prediction": "no_fraude",
    "probability": 0.51,
    "threshold_used": 0.7,
    "behavior_flags": {
        "unusual_response_rate": false,
        "unusual_mean_delay": false
    }
}
```

Payload de prueba (Fraude):
```powershell
{
  "client_id": "301",
  "amount": 750000.00,
  "tipo_transaccion": "compra",
  "channel_code": "WEB",
  "motor_monitoreo_map": "sospechoso",
  "alert_type": "compra_monto_alto",
  "dia_semana": 6,
  "client_mobilePhone": "3211111111",
  "response_text": "No",
  "timestamp": "2025-08-27T14:30:00",
  "total_sent": 15,
  "response_rate": 0.1,
  "mean_delay": 300
}
```

Esperado en respuesta:

```powershell
{
    "prediction": "fraude",
    "probability": 0.07,
    "threshold_used": 0.7,
    "behavior_flags": {
        "unusual_response_rate": true,
        "unusual_mean_delay": true
    }
}
```
---
## ✅ Notas
Siempre activar el entorno virtual antes de ejecutar scripts o FastAPI.
Ajustar el `.env` según tu base de datos y directorios de modelos.
Para ejecutar desde PowerShell sin errores de importación, establecer PYTHONPATH a la raíz del proyecto.
Testear con `pytest src/tests/` para verificar que todo funciona.