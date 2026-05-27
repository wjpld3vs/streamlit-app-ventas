# Clasificador Retail Inteligente - Dashboard Streamlit

Aplicacion web local desarrollada con **Streamlit** que utiliza un modelo de **Machine Learning (Random Forest)** para clasificar operaciones de venta retail como **Mayorista** o **Minorista**. Incluye modulos de prediccion individual, carga batch desde CSV, analisis del modelo y simulacion de escenarios.

---

## Novedades de esta version

| Modulo | Funcionalidad |
|--------|---------------|
| **Prediccion Individual** | Gauge de confianza, waterfall de contribucion por feature, recomendaciones accionables, graficos Plotly interactivos |
| **Carga por Lote (CSV)** | Procesamiento batch, KPIs de resumen, donut de clases, histograma de probabilidades, analisis temporal, exportacion de resultados |
| **Analisis del Modelo** | Feature importance, superficie de decision interactiva, matriz de confusion, curva ROC, metricas (accuracy, precision, recall, F1) |
| **Escenarios What-If** | Sliders en tiempo real, curvas de sensibilidad, comparador A/B |

---

## Estructura del proyecto

```
proyecto-streamlit-pkl/
├── app.py                              # Aplicacion principal (4 modulos)
├── modelo_clasificacion_retail.pkl     # Modelo RandomForest entrenado
├── requirements.txt                    # Dependencias Python (incluye Plotly)
├── README.md
├── docs/
│   └── streamlit_componentes.md        # Guia detallada de componentes
├── datos_prueba_50.csv                 # Dataset de prueba: 50 transacciones
├── datos_prueba_200.csv                # Dataset de prueba: 200 transacciones
└── datos_prueba_500.csv                # Dataset de prueba: 500 transacciones
```

---

## Instalacion y ejecucion

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repo>
cd proyecto-streamlit-pkl
```

### 2. Crear y activar el entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicacion

```bash
streamlit run app.py
```

La aplicacion se abrira en `http://localhost:8501`.

---

## Como usar las nuevas features

### Modulo 1: Prediccion Individual

1. En la barra lateral, ajuste los 3 parametros (**Cantidad kg**, **Precio Unitario**, **Descuento %**)
2. Presione **Clasificar Operacion**
3. Observe:
   - **Tarjeta de resultado** coloreada (rojo = Mayorista, azul = Minorista)
   - **Gauge de confianza** con zonas verde (>90%), amarilla (70-90%), roja (<70%)
   - **Waterfall de contribucion**: barras rojas = empujan hacia Mayorista, azules = hacia Minorista
   - **Acciones recomendadas** en el expander inferior, segmentadas por clase y nivel de confianza
4. Use el boton **Limpiar** para reiniciar

### Modulo 2: Carga por Lote (CSV)

1. Seleccione un **dataset de prueba** del dropdown o **suba su propio CSV**
   - Columnas requeridas: `cantidad_kg`, `precio_unitario`, `descuento_pct`
   - Columnas opcionales: `fecha` (para analisis temporal), `clase_real` (para metricas)
2. Los resultados se muestran automaticamente:
   - **KPI cards**: total transacciones, % Mayorista/Minorista, confianza media, importe total, zona gris
   - **Donut chart**: distribucion de clases
   - **Histograma**: distribucion de probabilidades predichas
   - **Barras apiladas**: confianza por clase
   - **Serie temporal**: evolucion diaria/semanal/mensual (si el CSV tiene `fecha`)
3. Use los **filtros** en la sidebar para segmentar por clase o nivel de confianza
4. Ajuste el **umbral de decision** para ver como cambia la clasificacion
5. Presione **Descargar resultados** para exportar el CSV con predicciones

### Modulo 3: Analisis del Modelo

1. Observe el grafico de **Feature Importance** que muestra que variables pesan mas
2. Explore la **superficie de decision** interactiva:
   - Mapa de calor que muestra como clasifica el modelo en el espacio cantidad vs precio
   - Use el slider de **descuento fijo** para ver como cambia la frontera
   - La linea blanca muestra el umbral de decision configurable
3. Seleccione un dataset con `clase_real` para ver **metricas de rendimiento**:
   - Accuracy, Precision, Recall, F1-Score
   - Matriz de confusion
   - Curva ROC con AUC
   - Reporte de clasificacion detallado

### Modulo 4: Escenarios What-If

**Modo Sliders en Tiempo Real:**
- Mueva los sliders y observe como la prediccion se actualiza instantaneamente
- Sin necesidad de presionar boton

**Modo Curva de Sensibilidad:**
- Seleccione una feature a variar y configure los valores fijos de las otras
- Observe la curva que muestra como cambia P(Mayorista) al variar la feature
- Identifique el **punto de cruce** donde el modelo cambia de Minorista a Mayorista

**Modo Comparador A/B:**
- Configure dos escenarios distintos lado a lado
- Compare clasificaciones, probabilidades e importes
- Vea las diferencias en tabla resumen y grafico comparativo

---

## Datasets de prueba incluidos

Tres archivos CSV pre-generados en la raiz del proyecto:

| Archivo | Transacciones | Periodo | Mayoristas reales | Minoristas reales |
|---------|---------------|---------|-------------------|-------------------|
| `datos_prueba_50.csv` | 50 | ene-feb 2026 | ~16 | ~34 |
| `datos_prueba_200.csv` | 200 | ene-abr 2026 | ~69 | ~131 |
| `datos_prueba_500.csv` | 500 | ene-jun 2026 | ~194 | ~306 |

Cada CSV incluye la columna `clase_real` con la clasificacion verdadera para evaluar el modelo.
La columna `fecha` permite analisis de tendencias temporales.

---

## Dependencias

```
streamlit>=1.45.0
scikit-learn>=1.6.0
joblib>=1.4.0
pandas>=2.2.0
numpy>=2.0.0
matplotlib>=3.10.0
plotly>=5.22.0
```

---

## Como extender el proyecto

- **Agregar nuevas features**: reentrene el modelo, actualice `COLUMNAS_MODELO` y los sliders en cada tab
- **Cambiar el modelo .pkl**: reemplace el archivo y actualice constantes
- **Agregar graficos**: use `st.plotly_chart()` con `plotly.graph_objects` o `plotly.express`
- **Nuevos modulos**: agregue opciones al `st.sidebar.radio` de navegacion y desarrolle la nueva seccion

---

## Buenas practicas

- Modelo cacheado con `@st.cache_resource`
- Validacion de CSV antes de procesar
- Manejo de errores en carga de modelo y predicciones
- Graficos interactivos con Plotly (tooltips, zoom, descarga)
- Estilos condicionales en tablas de resultados
- Session state para persistencia entre renderizados
