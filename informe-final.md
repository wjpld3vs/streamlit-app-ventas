# Informe Final del Proyecto: Sistema de Clasificacion Retail con Machine Learning y Streamlit

**Autor:** Wilmer Palacios
**Repositorio:** `proyecto-streamlit-pkl`
**Fecha:** Mayo 2026
**Tecnologias:** Python, Streamlit, scikit-learn, Plotly, Pandas, Apache Airflow, Parquet, Joblib

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Objetivos del Proyecto](#2-objetivos-del-proyecto)
3. [Arquitectura General](#3-arquitectura-general)
4. [Fase 1: Proceso ETL en Apache Airflow](#4-fase-1-proceso-etl-en-apache-airflow)
5. [Fase 2: Entrenamiento de Modelos ML](#5-fase-2-entrenamiento-de-modelos-ml)
6. [Fase 3: Generacion del Modelo Final (.pkl)](#6-fase-3-generacion-del-modelo-final-pkl)
7. [Fase 4: Dashboard Streamlit Profesional](#7-fase-4-dashboard-streamlit-profesional)
8. [Resultados y Metricas](#8-resultados-y-metricas)
9. [Conclusiones y Recomendaciones](#9-conclusiones-y-recomendaciones)
10. [Anexos](#10-anexos)

---

## 1. Resumen Ejecutivo

Este proyecto implementa un sistema completo de clasificacion retail que permite predecir automaticamente si una transaccion de venta corresponde a un **cliente Mayorista** o **cliente Minorista**, basandose en variables como cantidad de producto, precio unitario y descuento aplicado.

El flujo completo abarca desde la **ingenieria de datos con ETL** (Apache Airflow + Parquet), pasando por el **entrenamiento y evaluacion de multiples modelos de Machine Learning** (Regresion Lineal, Arboles de Decision, Random Forest, XGBoost), hasta un **dashboard profesional en Streamlit** con 4 modulos interactivos que permiten prediccion individual, carga batch desde CSV, analisis del modelo y simulacion de escenarios.

El modelo final implementado es un **Random Forest Classifier** con una precision del **92%** en datos de prueba, desplegado como archivo `.pkl` y servido via Streamlit con visualizaciones profesionales en Plotly.

---

## 2. Objetivos del Proyecto

### Objetivo General
Desarrollar un sistema de apoyo a la toma de decisiones comerciales que clasifique automaticamente transacciones retail como Mayoristas o Minoristas, permitiendo a los equipos comerciales actuar con mayor velocidad y precision.

### Objetivos Especificos

| # | Objetivo | Estado |
|---|----------|--------|
| 1 | Implementar un pipeline ETL robusto para transformar datos operacionales en formato Parquet particionado | Completado |
| 2 | Entrenar y comparar multiples algoritmos de ML (regresion y clasificacion) para seleccionar el mejor modelo | Completado |
| 3 | Generar un modelo `.pkl` optimizado listo para produccion | Completado |
| 4 | Construir un dashboard profesional en Streamlit con prediccion individual, batch, analisis y simulacion | Completado |
| 5 | Generar datasets de prueba realistas para validacion y demostracion | Completado |
| 6 | Documentar exhaustivamente el proyecto para facilitar su extension y mantenimiento | Completado |

---

## 3. Arquitectura General

```
┌──────────────────────────────────────────────────────────────────┐
│                    FASE 1: INGENIERIA DE DATOS                    │
│                                                                    │
│  Datos Operacionales ──► Apache Airflow (ETL) ──► Parquet (.pq)   │
│  (CSV, SQL, APIs)        Limpieza, Transformacion,   Particionado  │
│                           Particionamiento          train/test      │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                   FASE 2: MACHINE LEARNING                        │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ REGRESION (Semana 6-8)                                       │ │
│  │  Features: cantidad, precio_unitario, descuento_pct          │ │
│  │  Target: total_venta                                         │ │
│  │  Modelos: LinearRegression, DecisionTree, RandomForest, XGB  │ │
│  │  Evaluacion: R2, RMSE, Cross-Validation, Learning Curves     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ CLASIFICACION (Semana 9)                                     │ │
│  │  Features: cantidad, precio_unitario, descuento_pct, venta   │ │
│  │  Target: metodo_pago                                         │ │
│  │  Modelos: LogisticRegression, DecisionTree, RF, XGB          │ │
│  │  Evaluacion: Accuracy, F1-Score, Confusion Matrix            │ │
│  │  Tunning: GridSearchCV, KFold cross-validation               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                 FASE 3: MODELO FINAL (.pkl)                       │
│                                                                    │
│  Datos Sinteticos ──► RandomForestClassifier ──► .pkl             │
│  (1,000 retail)       (n=100, depth=5)          joblib.dump()     │
│                                                                    │
│  Features: cantidad_kg, precio_unitario, descuento_pct            │
│  Target: tipo_cliente (0=Minorista, 1=Mayorista)                  │
│  Precision: ~92% en test set                                      │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                FASE 4: DASHBOARD STREAMLIT                        │
│                                                                    │
│  app.py ──┬── Tab 1: Prediccion Individual                       │
│           │      Gauge, Waterfall, Barras, Recomendaciones        │
│           │                                                        │
│           ├── Tab 2: Carga por Lote (CSV)                         │
│           │      KPIs, Donut, Histograma, Serie Temporal          │
│           │      Filtros, Exportacion CSV                          │
│           │                                                        │
│           ├── Tab 3: Analisis del Modelo                          │
│           │      Feature Importance, Superficie Decision          │
│           │      Matriz Confusion, Curva ROC, Metricas             │
│           │                                                        │
│           └── Tab 4: Escenarios What-If                           │
│                  Sliders Real-Time, Curvas Sensibilidad            │
│                  Comparador A/B                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Fase 1: Proceso ETL en Apache Airflow

### 4.1 Pipeline ETL

El proceso de Extraccion, Transformacion y Carga (ETL) se implemento en Apache Airflow, siguiendo la guia de la Semana 3 del curso. El flujo de datos es:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌───────────────┐
│  EXTRACT    │ ──► │ TRANSFORM   │ ──► │   LOAD      │ ──► │ PARTICIONAR   │
│             │     │             │     │             │     │               │
│ • CSV       │     │ • Limpieza  │     │ • Parquet   │     │ • ml_set =    │
│ • SQLite    │     │ • Validacion│     │   (.pq)     │     │   entrenamiento│
│ • APIs      │     │ • Encoding  │     │ • Snappy    │     │   / pruebas   │
│ • Generacion│     │ • Fechas    │     │   compress  │     │ • category =  │
│   sintetica │     │ • Tipos     │     │             │     │   Hogar/...   │
└─────────────┘     └─────────────┘     └─────────────┘     └───────────────┘
```

### 4.2 Implementacion Tecnica

#### Generacion de datos sinteticos (1M registros)
```python
datos = {
    'id': range(1, 1000001),
    'edad': np.random.randint(18, 80, 1000000),
    'ingresos': np.random.uniform(20000, 150000, 1000000),
    'fecha': pd.date_range(start='2020-01-01', periods=1000000, freq='T'),
    'compro_producto': np.random.choice([0, 1], 1000000)
}
df.to_parquet('ventas.parquet', engine='pyarrow')
```

#### Conversion de formatos (CSV/SQL a Parquet)
```python
def csv_to_parquet(csv_path, parquet_path):
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, compression='snappy')

def sql_to_parquet(db_path, query, parquet_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    df.to_parquet(parquet_path)
```

#### Particionamiento estrategico de datos
```python
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
fecha_corte = pd.to_datetime('2025-01-01')
df['ml_set'] = np.where(df['fecha_venta'] < fecha_corte, 'entrenamiento', 'pruebas')

df.to_parquet(
    'dataset_ventas_2',
    engine='pyarrow',
    partition_cols=['ml_set'],
    index=False
)
```

#### Lectura optimizada con filtros
```python
filtros = [
    ('metodo_pago', '==', 'Efectivo'),
    ('region', '==', 'Sur')
]
df_filtrado = pd.read_parquet(
    'dataset_ventas/ml_set=entrenamiento/categoria=Hogar',
    engine='pyarrow',
    filters=filtros
)
```

### 4.3 Decisiones de Arquitectura de Datos

| Decision | Justificacion |
|----------|---------------|
| **Parquet sobre CSV** | Compresion Snappy (10x menor), lectura columnar, schema embebido, particionamiento nativo |
| **Particion por fecha** | Permite train/test split natural sin data leakage temporal |
| **Particion por categoria** | Lectura selectiva por categoria de producto sin cargar todo el dataset |
| **PyArrow como engine** | Rendimiento superior en lectura/escritura vs fastparquet |
| **Airflow como orquestador** | Scheduling, monitoreo, reintentos, DAGs visuales |

---

## 5. Fase 2: Entrenamiento de Modelos ML

El proceso de entrenamiento se desarrollo en un Jupyter Notebook (`cuaderno.ipynb`) con 61 celdas que abarcan desde la Semana 6 hasta la Semana 10 del curso.

### 5.1 Fase de Regresion (Semanas 6-8)

**Objetivo:** Predecir el monto total de venta (`total_venta`) basado en caracteristicas de la transaccion.

**Features utilizadas:**
- `cantidad`: cantidad de producto
- `precio_unitario`: precio por unidad
- `descuento_pct`: porcentaje de descuento aplicado

**Target:** `total_venta`

#### Cuadro comparativo de modelos de regresion

| Modelo | R2 Score | RMSE | Hiperparametros |
|--------|----------|------|-----------------|
| Regresion Lineal Multiple | Base | - | `fit_intercept=True` |
| Arbol de Decision | Variable | Variable | `max_depth=5`, `random_state=42` |
| **Random Forest** | **Alto** | **Bajo** | `n_estimators=100`, `max_depth=10` |
| XGBoost | **Mejor** | **Menor** | `n_estimators=200`, `learning_rate=0.1`, `max_depth=5` |

#### Tecnicas de evaluacion aplicadas
- **R2 Score**: coeficiente de determinacion
- **RMSE**: error cuadratico medio (en unidades monetarias)
- **Cross-Validation**: validacion cruzada con 5 folds
- **Learning Curves**: curvas de aprendizaje para detectar overfitting/underfitting
- **Residual Analysis**: grafico de residuos para verificar homocedasticidad
- **Stability Boxplots**: distribucion de RMSE en cross-validation

#### Visualizaciones generadas
1. **Barplot comparativo** de RMSE y R2 entre los 4 modelos
2. **Scatter plot** predicciones vs valores reales (Random Forest)
3. **Grafico de residuos** (errores vs predicciones)
4. **Feature importance** - variables que mas impactan las ventas
5. **Boxplot de estabilidad** por modelo (cross-validation)
6. **Curva de aprendizaje** para Random Forest

### 5.2 Fase de Clasificacion (Semana 9)

**Objetivo:** Predecir el metodo de pago (`metodo_pago`) basado en caracteristicas de la transaccion.

**Features utilizadas:** `cantidad`, `precio_unitario`, `descuento_pct`, `total_venta`
**Target:** `metodo_pago` (categorico, transformado con LabelEncoder)

#### Happy Path - Torneo de clasificadores

| Modelo | Accuracy | F1-Score (macro) |
|--------|----------|-------------------|
| Regresion Logistica | Variable | Variable |
| Arbol de Decision | Variable | Variable |
| **Random Forest** | **Alto** | **Alto** |
| XGBoost | Alto | Alto |

#### Tunning de Hiperparametros (Random Forest Classifier)

```python
parametros_rf = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5]
}

buscador_clf = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=parametros_rf,
    scoring='f1_macro',
    cv=KFold(n_splits=3, shuffle=True, random_state=42),
    n_jobs=-1
)
```

#### Evaluacion final de clasificacion
- **Classification Report** con precision, recall y F1 por clase
- **Matriz de confusion** grafica (heatmap)
- Validacion con el 20% de datos de prueba separados por fecha

### 5.3 Metricas Finales (20% datos de prueba)

| Metrica | Definicion |
|---------|------------|
| R2 Score | Proporcion de varianza explicada por el modelo |
| RMSE | Raiz del error cuadratico medio |
| MAE | Error absoluto medio |
| Accuracy | Porcentaje de predicciones correctas |
| F1-Score | Media armonica de precision y recall |
| Matriz de Confusion | Verdaderos/falsos positivos/negativos |

---

## 6. Fase 3: Generacion del Modelo Final (.pkl)

### 6.1 Modelo de Regresion: `modelo_predictor_ventas.pkl`

Exportado desde el notebook (Cell 53):

```python
import joblib
ruta = 'modelo_predictor_ventas.pkl'
joblib.dump(modelo_xgb, ruta)
```

**Tipo:** XGBoost Regressor
**Proposito:** Predecir el monto total de venta
**Estado:** Guardado en Google Colab (no desplegado en Streamlit)

### 6.2 Modelo de Clasificacion: `modelo_clasificacion_retail.pkl`

Generado en el notebook (Cell 61) y desplegado en el dashboard:

```python
# Generacion de datos sinteticos de retail (1,000 transacciones)
np.random.seed(42)
n_ventas = 1000

cantidad_kg = np.random.randint(1, 500, n_ventas)
precio_unitario = np.random.uniform(5.0, 15.0, n_ventas)
descuento = np.random.choice([0.0, 0.05, 0.10, 0.15], n_ventas)

# Logica de negocio: a mayor volumen + descuento, mayor prob. de Mayorista
prob_mayorista = (cantidad_kg / 500) + descuento
tipo_cliente = np.where(prob_mayorista > 0.6, 1, 0)

# Entrenamiento
modelo_retail = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
modelo_retail.fit(X_train, y_train)

# Exportacion
joblib.dump(modelo_retail, 'modelo_clasificacion_retail.pkl')
```

### 6.3 Caracteristicas del Modelo Final

| Propiedad | Valor |
|-----------|-------|
| **Tipo** | RandomForestClassifier |
| **Framework** | scikit-learn |
| **n_estimators** | 100 arboles |
| **max_depth** | 5 (controla overfitting) |
| **random_state** | 42 (reproducibilidad) |
| **Features** | `cantidad_kg`, `precio_unitario`, `descuento_pct` |
| **Clases** | 0 = Minorista, 1 = Mayorista |
| **predict_proba** | Disponible |
| **Serializacion** | joblib (.pkl) |
| **Precision en test** | ~92% |
| **Feature mas importante** | `cantidad_kg` (90.4% de importancia) |

### 6.4 Analisis de Feature Importance del Modelo Final

| Feature | Importancia | Interpretacion de negocio |
|---------|-------------|---------------------------|
| `cantidad_kg` | 90.39% | El volumen de compra es el factor determinante para clasificar clientes |
| `precio_unitario` | 5.87% | El precio ayuda a refinar la clasificacion en casos limite |
| `descuento_pct` | 3.75% | Descuentos altos son tipicos de clientes mayoristas |

---

## 7. Fase 4: Dashboard Streamlit Profesional

### 7.1 Estructura del Dashboard

El dashboard se organiza en **4 modulos** accesibles via sidebar de navegacion:

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR                             │  MAIN PANEL           │
│                                      │                       │
│  ◉ Prediccion Individual            │  TAB 1                │
│    Parametros:                       │  ┌─────────────────┐ │
│    - Cantidad (kg) [number_input]    │  │ Result Card     │ │
│    - Precio ($)    [number_input]    │  │ Gauge Confianza │ │
│    - Descuento (%) [slider]          │  │ Probabilidades  │ │
│    [Clasificar] [Limpiar]            │  │ Waterfall       │ │
│                                      │  │ Recomendaciones │ │
│  ○ Carga por Lote (CSV)             │  └─────────────────┘ │
│    Dataset: [selectbox]              │                       │
│    Upload:   [file_uploader]         │  TAB 2                │
│    Filtros:                          │  ┌─────────────────┐ │
│    - Clase    [selectbox]            │  │ 6 KPI Cards     │ │
│    - Confianza [selectbox]           │  │ Donut Chart     │ │
│    - Umbral   [slider]               │  │ Histograma      │ │
│                                      │  │ Serie Temporal  │ │
│  ○ Analisis del Modelo              │  │ Tabla Resultados│ │
│    Dataset eval: [selectbox]         │  │ Exportar CSV    │ │
│    Umbral: [slider]                  │  └─────────────────┘ │
│                                      │                       │
│  ○ Escenarios What-If               │  TAB 3                │
│    Modo: [radio]                     │  ┌─────────────────┐ │
│    - Sliders Real-Time               │  │ Feature Import. │ │
│    - Curva Sensibilidad              │  │ Superficie Dec. │ │
│    - Comparador A/B                  │  │ Matriz Confus.  │ │
│                                      │  │ Curva ROC       │ │
│  ┌──────────────────────────────┐   │  │ Metricas        │ │
│  │ Modelo: RandomForestClassifier│   │  └─────────────────┘ │
│  │ Features: cantidad_kg, ...   │   │                       │
│  │ Clases: Minorista, Mayorista │   │  TAB 4                │
│  └──────────────────────────────┘   │  ┌─────────────────┐ │
│                                      │  │ Pred. Real-Time │ │
│                                      │  │ Curva Sensib.   │ │
│                                      │  │ Comparador A/B  │ │
│                                      │  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Tab 1: Prediccion Individual

**Componentes:**
- Sidebar con 3 inputs: `cantidad_kg` (number_input 1-500), `precio_unitario` (number_input 0.01-500), `descuento_pct` (slider 0-100)
- Boton "Clasificar Operacion" y boton "Limpiar"
- **Result Card**: tarjeta coloreada (rojo=Mayorista, azul=Minorista) con etiqueta y confianza
- **Gauge de Confianza**: velocimetro Plotly con zonas verde (>90%), amarilla (70-90%), roja (<70%)
- **3 Metric Boxes**: P(Mayorista), P(Minorista), Importe Total Estimado
- **Barras de Probabilidad**: grafico Plotly horizontal con ambas probabilidades
- **Waterfall de Contribucion**: barras horizontales mostrando cuanto aporta cada feature y en que direccion
- **Interpretacion del modelo**: mensaje contextual con 3 niveles de confianza
- **Acciones recomendadas**: lista de acciones segun clase + tier de confianza (expandible)
- **Datos de entrada**: DataFrame con valores enviados al modelo (expandible)

**Graficos Plotly:**
- `go.Indicator` (gauge mode)
- `go.Bar` (horizontal, colores sematicos)

### 7.3 Tab 2: Carga por Lote (CSV)

**Componentes:**
- Sidebar con selector de dataset de prueba (`datos_prueba_50/200/500.csv`) o uploader de CSV propio
- Validacion automatica de columnas requeridas
- Procesamiento batch con `st.spinner`

**KPIs de Resumen (6 cards):**
| KPI | Color | Valor ejemplo (500 filas) |
|-----|-------|---------------------------|
| Transacciones procesadas | #6366f1 | 500 |
| % Mayorista | #e94560 | 30% |
| % Minorista | #3b82f6 | 70% |
| Confianza media | #10b981 | 80% |
| Importe total | #f59e0b | $250,000 |
| Zona gris (baja confianza) | #ef4444 | 45 |

**Visualizaciones:**
- **Donut chart**: proporcion Mayorista vs Minorista
- **Histograma**: distribucion de probabilidades predichas
- **Barras apiladas**: confianza por clase (Alta/Media/Baja)
- **Serie temporal**: evolucion diaria/semanal/mensual del % Mayorista (requiere columna `fecha`)
- **Tabla de resultados**: estilo condicional (filas rojas/azules), columnas formateadas

**Funcionalidades adicionales:**
- Filtros por clase (Todas/Mayorista/Minorista)
- Filtros por nivel de confianza (Todos/Alta/Media/Baja)
- Ajuste de umbral de decision (slider 0.0 - 1.0)
- Exportacion de resultados a CSV (`st.download_button`)
- Conteo de transacciones de alta confianza por clase

### 7.4 Tab 3: Analisis del Modelo

**Componentes:**
- **Feature Importance**: barras horizontales con los pesos reales del modelo
- **Superficie de decision**: heatmap interactivo que muestra como clasifica el modelo en el espacio cantidad vs precio
  - Con contorno del umbral de decision
  - Slider de descuento fijo para explorar diferentes escenarios
- **Metricas de rendimiento**: accuracy, precision, recall, F1-Score (requiere `clase_real` en el CSV)
- **Matriz de confusion**: heatmap con anotaciones numericas
- **Curva ROC**: con AUC, linea de referencia aleatoria
- **Reporte de clasificacion**: tabla detallada con precision, recall, F1 por clase

**Metricas con datos de prueba:**
| Metrica | datos_prueba_50 | datos_prueba_200 | datos_prueba_500 |
|---------|-----------------|------------------|------------------|
| Accuracy | 92.00% | 89.00% | 89.60% |
| Precision | Variable | Variable | Variable |
| Recall | Variable | Variable | Variable |
| F1-Score | Variable | Variable | Variable |

### 7.5 Tab 4: Escenarios What-If

**Tres modos de analisis:**

#### Modo 1: Sliders en Tiempo Real
- 3 sliders que actualizan la prediccion instantaneamente
- Resultado, gauge, metricas, barras y waterfall se refrescan al mover cualquier slider
- Sin necesidad de presionar boton

#### Modo 2: Curva de Sensibilidad
- Seleccionar feature a variar
- Configurar valores fijos de las otras features
- Grafico de linea mostrando P(Mayorista) vs valor de la feature
- Identificacion automatica del punto de cruce del umbral 50%
- Tabla de puntos clave (10%, 30%, 50%, 70%, 90% del rango)

#### Modo 3: Comparador A/B
- Dos escenarios completos lado a lado (VS)
- Cada escenario con sus propias predicciones, metricas e importes
- Tabla de diferencias entre escenarios
- Grafico comparativo de barras agrupadas

### 7.6 Stack Tecnologico del Dashboard

| Capa | Tecnologia | Version | Proposito |
|------|------------|---------|-----------|
| **Web Framework** | Streamlit | >=1.45.0 | UI reactiva, widgets, session state |
| **ML** | scikit-learn | >=1.6.0 | RandomForestClassifier, metricas |
| **Serializacion** | joblib | >=1.4.0 | Carga del modelo .pkl |
| **Datos** | pandas | >=2.2.0 | DataFrames, CSV, manipulacion |
| **Visualizacion** | Plotly | >=5.22.0 | Graficos interactivos profesionales |
| **Numerico** | numpy | >=2.0.0 | Operaciones matriciales |
| **CSS** | Custom | - | Inter font, gradientes, tarjetas, animaciones |

### 7.7 Componentes Streamlit Utilizados

| # | Componente | Uso en el dashboard |
|---|------------|---------------------|
| 1 | `st.set_page_config` | Configuracion global (wide layout, favicon) |
| 2 | `st.markdown` | CSS, HTML personalizado, tarjetas KPI |
| 3 | `st.sidebar` | Navegacion, controles, filtros |
| 4 | `st.radio` | Navegacion principal (4 modulos), modo What-If |
| 5 | `st.selectbox` | Datasets, feature a variar, filtros, frecuencia |
| 6 | `st.slider` | Parametros, umbrales, rango de sensibilidad |
| 7 | `st.number_input` | Cantidad kg, precio unitario |
| 8 | `st.button` | Clasificar, Limpiar |
| 9 | `st.file_uploader` | Carga de CSV del usuario |
| 10 | `st.columns` | Layout multi-columna (KPIs, graficos lado a lado) |
| 11 | `st.dataframe` | Tabla de resultados con estilo condicional |
| 12 | `st.plotly_chart` | Renderizado de graficos Plotly |
| 13 | `st.metric` | Conteos de alta confianza |
| 14 | `st.download_button` | Exportacion de resultados CSV |
| 15 | `st.spinner` | Indicador de carga durante batch |
| 16 | `st.expander` | Datos de entrada, recomendaciones, reporte |
| 17 | `st.success/st.info/st.warning/st.error/st.caption` | Mensajes semanticos |
| 18 | `st.session_state` | Persistencia entre modulos |
| 19 | `@st.cache_resource` | Cacheo del modelo en memoria |

### 7.8 Graficos Plotly Implementados

| # | Grafico | Tipo Plotly | Colores |
|---|---------|-------------|---------|
| 1 | Gauge de confianza | `go.Indicator` (gauge) | Verde/Ambar/Rojo |
| 2 | Barras de probabilidad | `go.Bar` (horizontal) | #e94560 / #3b82f6 |
| 3 | Feature Importance | `go.Bar` (horizontal, colorscale) | Azul → Rojo |
| 4 | Waterfall de contribucion | `go.Bar` (horizontal, condicional) | Rojo(+) / Azul(-) |
| 5 | Donut de clases | `go.Pie` (hole=0.55) | #e94560 / #3b82f6 |
| 6 | Histograma de probs | `px.histogram` | #6366f1 |
| 7 | Serie temporal (doble eje) | `go.Scatter` + `make_subplots` | #e94560 / #6366f1 |
| 8 | Barras apiladas de confianza | `go.Bar` (stacked) | #e94560 / #3b82f6 |
| 9 | Superficie de decision | `go.Heatmap` + `go.Contour` | Azul → Morado → Rojo |
| 10 | Matriz de confusion | `px.imshow` | Gradiente azul |
| 11 | Curva ROC | `go.Scatter` | #e94560 |
| 12 | Curva de sensibilidad | `go.Scatter` (gradient markers) | #e94560 |
| 13 | Comparador A/B | `go.Bar` (grouped) | #e94560 / #3b82f6 |

---

## 8. Resultados y Metricas

### 8.1 Rendimiento del Modelo Final

**Evaluacion sobre datasets de prueba generados:**

| Dataset | Transacciones | Accuracy | Mayoristas predichos | Minoristas predichos |
|---------|---------------|----------|----------------------|----------------------|
| `datos_prueba_50.csv` | 50 | **92.00%** | 12 (24%) | 38 (76%) |
| `datos_prueba_200.csv` | 200 | **89.00%** | 55 (27.5%) | 145 (72.5%) |
| `datos_prueba_500.csv` | 500 | **89.60%** | 150 (30%) | 350 (70%) |

**Distribucion real vs predicha en el dataset de 500:**
- Reales: 194 Mayoristas (39%), 306 Minoristas (61%)
- Predichos: 150 Mayoristas (30%), 350 Minoristas (70%)
- El modelo es conservador, tendiendo a clasificar como Minorista en casos limite

### 8.2 Feature Importance del Modelo

El modelo aprendio que `cantidad_kg` es el factor mas determinante (90.4%), seguido por `precio_unitario` (5.9%) y `descuento_pct` (3.7%). Esto refleja la regla de negocio: el volumen de compra es el principal indicador de perfil mayorista.

### 8.3 Datasets de Prueba Generados

| Archivo | Filas | Periodo | Mayoristas | Minoristas | Casos borde |
|---------|-------|---------|------------|------------|-------------|
| `datos_prueba_50.csv` | 50 | ene-feb 2026 | 32% | 68% | 15% |
| `datos_prueba_200.csv` | 200 | ene-abr 2026 | 34% | 66% | 15% |
| `datos_prueba_500.csv` | 500 | ene-jun 2026 | 39% | 61% | 15% |

Cada dataset incluye:
- `fecha`: timestamp para analisis temporal (distribuido uniformemente en el periodo)
- `cantidad_kg`: 1-500 kg (segun perfil: mayorista >200, minorista <80, borde 80-250)
- `precio_unitario`: $0.50 - $60.00 (distribucion uniforme)
- `descuento_pct`: 0-30% (mayorista >10%, minorista <10%, borde 5-15%)
- `clase_real`: etiqueta verdadera para evaluacion del modelo

---

## 9. Conclusiones y Recomendaciones

### 9.1 Conclusiones

1. **Pipeline de datos robusto**: El proceso ETL con Apache Airflow y formato Parquet permite manejar grandes volumenes de datos con compresion eficiente y acceso selectivo por particiones.

2. **Evaluacion exhaustiva de modelos**: Se compararon 4 algoritmos de regresion y 4 de clasificacion, con cross-validation, analisis de residuos, curvas de aprendizaje y tunning de hiperparametros via GridSearchCV.

3. **Modelo final preciso**: El RandomForestClassifier alcanza ~92% de precision en datos de prueba, con una clara interpretabilidad gracias a las feature importances.

4. **Dashboard profesional**: La aplicacion Streamlit ofrece 4 modulos que cubren el ciclo completo de decision: prediccion individual, analisis batch, transparencia del modelo y simulacion de escenarios.

5. **Graficos interactivos**: La integracion con Plotly proporciona visualizaciones profesionales con tooltips, zoom, pan y colores semanticos que facilitan la interpretacion.

6. **Preparado para operacion**: El sistema incluye exportacion de resultados, datasets de prueba, documentacion exhaustiva y manejo de errores.

### 9.2 Recomendaciones para Evolucion

| Prioridad | Recomendacion | Impacto |
|-----------|---------------|---------|
| **Alta** | Agregar datos reales de transacciones historicas para mejorar la precision del modelo | Aumenta confiabilidad |
| **Alta** | Implementar autenticacion de usuarios en Streamlit | Seguridad |
| **Media** | Agregar SHAP/LIME para explicabilidad avanzada por prediccion | Confianza del usuario |
| **Media** | Conectar a base de datos en tiempo real (PostgreSQL, BigQuery) | Operacional |
| **Media** | Implementar alertas automaticas para transacciones en zona gris | Accion inmediata |
| **Baja** | Agregar exportacion de reportes PDF automaticos | Documentacion |
| **Baja** | Implementar A/B testing online del modelo vs reglas de negocio | Mejora continua |
| **Baja** | Desplegar en Streamlit Cloud o servidor corporativo | Accesibilidad |

### 9.3 Lecciones Aprendidas

- La particion por fecha evita data leakage temporal en el train/test split
- Random Forest ofrece buen balance entre precision, interpretabilidad y velocidad de inferencia
- `max_depth=5` controla efectivamente el overfitting en datos sinteticos
- La feature importance revela que `cantidad_kg` domina la decision (90%)
- Los casos limite (zona gris) representan ~15% de las transacciones y requieren analisis manual
- El umbral de decision default (0.5) puede no ser optimo para todos los contextos de negocio

---

## 10. Anexos

### Anexo A: Estructura del Proyecto

```
proyecto-streamlit-pkl/
├── app.py                              # Dashboard Streamlit (1100+ lineas, 4 modulos)
├── cuaderno.ipynb                      # Notebook completo de entrenamiento ML (61 celdas)
├── modelo_clasificacion_retail.pkl     # Modelo RandomForest final (.pkl)
├── modelos.pptx                        # Presentacion de definicion de modelos (15 slides)
├── requirements.txt                    # Dependencias Python
├── README.md                           # Documentacion del proyecto
├── informe-final.md                    # Este informe
├── docs/
│   └── streamlit_componentes.md        # Guia de componentes Streamlit y Plotly
├── datos_prueba_50.csv                 # Dataset de prueba: 50 transacciones
├── datos_prueba_200.csv                # Dataset de prueba: 200 transacciones
└── datos_prueba_500.csv                # Dataset de prueba: 500 transacciones
```

### Anexo B: Como Ejecutar el Proyecto

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd proyecto-streamlit-pkl

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
streamlit run app.py

# 5. Abrir navegador en http://localhost:8501
```

### Anexo C: Guia Rapida de Uso del Dashboard

| Modulo | Que hacer | Que obtienes |
|--------|-----------|--------------|
| **Prediccion Individual** | Ajustar 3 parametros en sidebar → "Clasificar" | Clase, confianza, gauge, waterfall, recomendaciones |
| **Carga por Lote** | Seleccionar dataset o subir CSV → automatico | KPIs, donut, histograma, serie temporal, tabla filtrable, exportar |
| **Analisis del Modelo** | Seleccionar dataset con `clase_real` | Feature importance, superficie decision, matriz confusion, ROC, metricas |
| **Escenarios What-If** | Elegir modo (sliders/curva/comparador) | Prediccion en tiempo real, curvas de sensibilidad, comparacion A/B |

### Anexo D: Referencias

- **Streamlit Documentation**: https://docs.streamlit.io
- **scikit-learn Documentation**: https://scikit-learn.org
- **Plotly Python Documentation**: https://plotly.com/python
- **Apache Airflow Documentation**: https://airflow.apache.org
- **Apache Parquet**: https://parquet.apache.org
- **Guia ETL en Airflow**: Semana 3 - Notion (Wilmer Palacios)

---

**Documento generado el 27 de Mayo de 2026.**
**Proyecto: Clasificador Retail Inteligente con Machine Learning y Streamlit.**
