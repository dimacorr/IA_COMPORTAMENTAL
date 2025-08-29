# 🔎 Proyecto de Detección de Fraude con IA Comportamental

Este proyecto implementa un modelo de **Machine Learning** para identificar comportamientos anómalos en transacciones de 
clientes, con el objetivo de prevenir fraude y reducir riesgos operativos.

La documentación está dividida en dos visiones:
  * **Funcional:** Qué problema resuelve y el beneficio para la organización. 
  * **Técnica:** Cómo funciona la solución y cómo desplegarla.
---

## 🚀 Visión Funcional (Negocio)
1. **Objetivo**</br>
   Detectar en tiempo real clientes o transacciones con patrones inusuales para prevenir actividades fraudulentas.
2. **Beneficios**
   * Anticipar actividades fraudulentas antes de que ocurran. 
   * Disminuir falsos positivos (no bloquear clientes legítimos). 
   * Automatizar la detección en tiempo real, mejorando la seguridad y experiencia del cliente.
2. **Ejemplo de uso**</br>
   Si un cliente normalmente responde rápido en horarios laborales, pero de repente empieza a interactuar a medianoche  
   con grandes retrasos, el modelo lo marcará como alerta para revisión.
---

## 🛠️ Visión Técnica (Flujo del Proyecto)
1. **Carga de datos** 
   * **Fuente:** base de datos Postgres (envios_cliente, transacciones). 
   * **Campos clave:** cliente, transacción, hora de envío, canal, respuesta.
2. **Feature Engineering (ingeniería de características)**
   * Conversión de hora a valores numéricos. 
   * Días de la semana.
   * Retraso entre envío y respuesta.
   * Tasas de respuesta.
   * Flags de comportamiento inusual (ej. respuestas demasiado tardías). <br>
   👉 Permite que el modelo capture patrones de riesgo de forma cuantitativa.
3. **Entrenamiento del modelo**
   * **Algoritmo:** `RandomForestClassifier` con balanceo de clases.
   * **Variable objetivo:**
     * `1` → Transacción sospechosa (alerta o declinada).
     * `0` → Transacción normal (confirmada).
4. **Evaluación del rendimiento**
   * **ROC AUC: ** mide la capacidad para distinguir fraude de no fraude
   * **Reporte de clasificación: ** precisión, recall y F1-score.<br>
     👉 Métricas que aseguran objetivamente la calidad del modelo.
5. **Persistencia del modelo**
   * El modelo entrenado se guarda en: `models/model.pkl.`
   * Se almacenan las features en: `models/features.pkl.`
   * Garantiza coherencia entre entrenamiento y predicciones en producción.

---

#### 📌 En resumen: El sistema transforma datos de comportamiento en señales cuantitativas, entrena un modelo, lo 
valida con métricas objetivas y lo despliega para predecir en tiempo real.
---

## 🛠️ Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes programas:

1. Python 3.10+ 
2. PostgreSQL 
3. pip y psql 
4. Git (opcional para clonar el repo)

#### 📌 Importante: asegúrate de que Python y PostgreSQL estén en el PATH del sistema, sin importar si usas Windows, Linux o MacOS.

---

## 🏗️ Configuración del entorno
Sigue estos pasos para preparar el proyecto:

1. **Crear entorno virtual:**
```powershell
 python -m venv .venv
 .venv\Scripts\activate      # Windows
 # source .venv/bin/activate # Linux/Mac
```

2. **Instalar dependencias:**
```powershell
 pip install -r requirements.txt
```

3. **Crear base de datos y tablas:**
```bash
 psql -U <usuario> -d <nombre_base_datos> -f sql/schema.sql
```

#### 📌 Nota:
* El usuario debe tener permisos para crear bases y tablas.
* DATABASE_URL en `.env` debe apuntar a esta base de datos.

4. **Configurar `.env:`**
```powershell
 DATABASE_URL=postgresql://user:password@host:port/db
 MODEL_DIR=models
 THRESHOLD=0.7
```

5. **Entrenar modelo (opcional):**
```powershell  
 python -m scripts.train
```

6. **Ejecutar aplicación:**  
```bash
 uvicorn main:app --reload
```

Endpoint de predicción:
```bash
 POST http://127.0.0.1:8000/predict
```
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
## 📖 Glosario de términos clave
 * **Machine Learning:** Rama de la inteligencia artificial que permite a los sistemas aprender de los datos y hacer 
   predicciones sin ser programados explícitamente. En este proyecto se utiliza para detectar patrones de 
   comportamiento y posibles fraudes.
 * **Feature Engineering:** Proceso de transformación de los datos crudos en variables (features) útiles para el 
   entrenamiento del modelo. Aquí se generan señales cuantitativas como `hour`, `weekday`, `response_rate`, etc.
 * **Predicción:** Proceso en el que el modelo entrenado clasifica nuevos datos para determinar si corresponden a 
   comportamiento normal o posible fraude.
 * **RandomForestClassifier:** Algoritmo de clasificación basado en múltiples árboles de decisión, 
   usado en este proyecto como modelo principal por su robustez y capacidad de manejar desbalance de clases.
 * **ROC AUC (Receiver Operating Characteristic - Area Under Curve):** Métrica que mide la capacidad del modelo para 
   distinguir entre clases (fraude vs. no fraude). Un valor cercano a 1 indica un mejor desempeño.
 * **Precisión (Precision):** Proporción de casos predichos como positivos que realmente lo son. 
   Evalúa qué tan “exactas” son las alertas generadas por el modelo.
 * **Recall (Sensibilidad o Exhaustividad):** Proporción de positivos reales que fueron correctamente detectados 
   por el modelo. Mide la capacidad de detectar fraudes sin que se escapen.
 * **F1-Score:**  Métrica que combina precisión y recall en un solo valor armónico. Es útil cuando hay desbalance 
   en las clases (fraude vs. no fraude).
   👉 Un F1-score alto significa que el modelo detecta la mayoría de fraudes sin generar demasiados falsos positivos.
 * **Threshold (Umbral de decisión):** Valor de corte de probabilidad para clasificar si una transacción es fraude (1) 
   o no (0). Un umbral más bajo detecta más fraudes, pero aumenta falsos positivos.

---
## ✅ Notas finales
 * Activa el entorno virtual antes de usar scripts o FastAPI. 
 * Ajusta el `.env` según tu configuración. 
 * Usa pytest src/tests/ para verificar que todo funciona.