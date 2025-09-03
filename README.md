# 🔎 Proyecto: IA para Detección de Comportamiento Transaccional
El fraude hoy es cada vez más dinámico y sofisticado.  Las reglas fijas, que antes alcanzaban, ya no son suficientes.
Por eso, este proyecto nace con el propósito de:
* Detectar tempranamente comportamientos atípicos,
* Fortalecer la gestión de fraude con Machine Learning,
* Y apoyar la toma de decisiones para dar más confianza en los procesos de validación.

## 🚀 Descripción del Proyecto
El sistema toma datos transaccionales almacenados en PostgreSQL, los procesa y entrena un modelo de Machine Learning.
El modelo entrenado se guarda en un archivo con Pickle y luego se utiliza para predecir en tiempo real si una nueva 
transacción es legítima o sospechosa.

####  ⚠️ Nota importante:
* El modelo se aplica en tiempo real (predicción sobre cada nueva transacción).
* El modelo no se reentrena en tiempo real; el reentrenamiento se hace en procesos batch programados. 
* Para reentrenar en cada transacción se necesitaría un esquema de online learning, lo cual no es el caso actual.

## 📊 Variables utilizadas en el modelo
* El modelo se alimenta de varias variables transaccionales clave:
* Monto de la transacción (amount)
* Tipo de transacción (tipo_transaccion)
* Hora de la transacción (hora_decimal)
* Canal de la transacción (channel_code)
* Día de la semana (dia_semana)
* Código de monitoreo (motor_monitoreo_map)
* Tipo de alerta (alert_type)
* Teléfono del cliente (client_mobilePhone)

🔎 Estas variables permiten identificar patrones de normalidad y anormalidad en las transacciones.

## 🧮 Modelo de Machine Learning
Se utiliza un `RandomForestClassifier`, un algoritmo basado en múltiples árboles de decisión que:
* Promedia la decisión de muchos árboles → más robustez.
* Tolera variables ruidosas mejor que otros modelos.
* Maneja bien datos categóricos y numéricos. 

##### Ventajas
* Buena precisión.
* Resistente al overfitting en comparación con un solo árbol.
* Capacidad de manejar muchas variables.

##### Limitaciones
* Si se incluyen muchas variables irrelevantes, puede introducir ruido.
* Modelos más simples (ej: Regresión Logística) pueden ser más interpretables.
* Modelos más avanzados (ej: XGBoost / LightGBM) pueden superar su precisión si se configuran bien.

## ⚠️ Overfitting (Sobreajuste)
El overfitting ocurre cuando el modelo "memoriza" los datos de entrenamiento en lugar de aprender patrones generales. </br>
Esto significa que:
* Funciona muy bien en el dataset de entrenamiento.
* Falla cuando llegan transacciones nuevas (datos que no había visto antes).

#### Cómo se mitiga:

* Más datos de entrenamiento (más transacciones históricas).
* Regularización del modelo (limitar la profundidad de árboles, número de árboles, etc.).
* Selección de variables → usar solo las que realmente aportan.

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

#### 📌 En resumen: El sistema transforma datos de comportamiento en señales cuantitativas, entrena un modelo, lo 
valida con métricas objetivas y lo despliega para predecir en tiempo real.

## 🛠️ Prerrequisitos
Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes programas:
1. Python 3.10+ 
2. PostgreSQL 
3. pip y psql 
4. Git (opcional para clonar el repo)

#### 📌 Importante: asegúrate de que Python y PostgreSQL estén en el PATH del sistema, sin importar si usas Windows, 
Linux o MacOS.

👉 Ejemplos de rutas que deben agregarse al PATH:
* **Python** → C:\Users\<tu-usuario>\AppData\Local\Programs\Python\Python310\Scripts\
* **PostgreSQL** → C:\Program Files\PostgreSQL\15\bin\

Esto permite que `python`, `pip` y `psql` se ejecuten desde cualquier consola.

## 🚀 Instalación y requisitos
1. **Clonar el repositorio:**
```bash
  git clone https://github.com/tu-repo/IA_COMPORTAMENTAL.git
  cd IA_COMPORTAMENTAL
```

2. **Crear entorno virtual:**
```powershell
 # Crear entorno virtual
 python -m venv .venv
 
 # Activar entorno virtual
 # Windows (PowerShell)
 .venv\Scripts\activate      
 
 # Windows (Git Bash) / Linux / MacOS
 source .venv/Scripts/activate
 # o
 source .venv/bin/activate
```

3. **Instalar dependencias:**
```powershell
 pip install -r requirements.txt
```

4. **Crear base de datos y tablas:**
```bash
 psql -U <usuario> -d <nombre_base_datos> -f sql/schema.sql
```

#### 📌 Nota: Antes de ejecutar el proyecto, asegúrate de tener PostgreSQL corriendo localmente, 
de crear la base de datos, las tablas necesarias, y ejecutar el script SQL incluido

5. **Configurar `.env:`**
```powershell
 # .env (ejemplo sin credenciales reales)
 DATABASE_URL=postgresql://user:password@host:port/db
 MODEL_DIR=models
 THRESHOLD=0.7
```

5. **Entrenar modelo (opcional):**
```powershell  
 python -m scripts.train
```

6. **Levantar API con FastAPI:**  
```bash
 uvicorn main:app --reload
```

Documentación interactiva:
```bash
 POST http://127.0.0.1:8000/predict
```

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
  "client_id": "201",              // Identificador único del cliente
  "amount": 150000,                // Monto de la transacción
  "tipo_transaccion": "compra",    // Tipo de transacción (ej: compra, retiro, transferencia)
  "channel_code": "WEB",           // Canal usado (WEB, ATM, APP, POS, etc.)
  "motor_monitoreo_map": "normal", // Categoría de monitoreo asignada por reglas previas
  "alert_type": "compra_estandar", // Tipo de alerta generada (ej: compra_estandar, alto_monto, etc.)
  "dia_semana": 2,                 // Día de la semana (0=Lunes, 6=Domingo) → útil para patrones
  "client_mobilePhone": "3202222222", // Teléfono del cliente (puede ser ruidoso si no aporta patrón)
  "response_text": "Sí",           // Respuesta del cliente (ej: "Sí fui yo", "No reconozco")
  "timestamp": "2025-08-25T10:00:00", // Fecha y hora de la transacción
  "total_sent": 1,                 // Número de mensajes enviados al cliente
  "response_rate": 1.0,            // Proporción de respuestas del cliente (0.0 a 1.0)
  "mean_delay": 1000                 // Tiempo promedio de demora en responder (en minutos/segundos)
}
```

Esperado en respuesta:

```powershell
{
    "prediction": "fraude",
    "probability": 0.27,
    "threshold_used": 0.7,
    "behavior_flags": {
        "unusual_response_rate": false,
        "unusual_mean_delay": true
    }
}
```

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
   en las clases (fraude vs. no fraude). </br>
   👉 Un F1-score alto significa que el modelo detecta la mayoría de fraudes sin generar demasiados falsos positivos.
 * **Threshold (Umbral de decisión):** Valor de corte de probabilidad para clasificar si una transacción es fraude (1) 
   o no (0). Un umbral más bajo detecta más fraudes, pero aumenta falsos positivos.
 * **Arquitectura Limpia (Clean Architecture):** Patrón de diseño que organiza el proyecto en capas separando lógica de 
   negocio (domain, usecases) de la infraestructura y adaptadores. Permite mayor mantenibilidad y escalabilidad.

## ❓ Explicación del Modelo (FAQ)
1. **¿Qué pasa si agrego variables no relevantes o muy relevantes?**
* No relevantes → generan ruido, pueden bajar la precisión del modelo.
* Relevantes → mejoran el desempeño porque aportan más señales útiles.
2. **¿Cómo puedo jugar con las variables?**
* Agregar o quitar variables en feature_engineering.py.
* Probar diferentes combinaciones de features.
* Evaluar importancia de variables con el propio Random Forest.
3. **¿El modelo mejora con más información?**
Sí. Más registros históricos permiten al modelo aprender mejor, generalizar y reducir sesgos.
4. **¿Cómo se estandarizan los datos?**
En este proyecto no aplicamos normalización numérica, ya que el algoritmo Random Forest no depende de la escala de los datos.
Lo que sí realizamos es feature engineering y preprocesamiento, transformando variables categóricas a numéricas, 
generando nuevas variables derivadas y limpiando los datos antes del entrenamiento.

## ✅ Notas finales
 * Activa el entorno virtual antes de usar scripts o FastAPI. 
 * Ajusta el `.env` según tu configuración. 
 * Usa pytest src/tests/ para verificar que todo funciona.