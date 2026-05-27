# Documentacion de Componentes Streamlit Utilizados

Guia tecnica de cada componente de Streamlit implementado en el dashboard de Clasificacion Retail v2. Incluye tanto los componentes nativos de Streamlit como la integracion con Plotly para graficos interactivos.

---

## Tabla de Contenidos

1. [st.set_page_config](#stset_page_config)
2. [st.markdown](#stmarkdown)
3. [st.sidebar](#stsidebar)
4. [st.radio](#stradio)
5. [st.number_input](#stnumber_input)
6. [st.slider](#stslider)
7. [st.button](#stbutton)
8. [st.selectbox](#stselectbox)
9. [st.file_uploader](#stfile_uploader)
10. [st.columns](#stcolumns)
11. [st.dataframe](#stdataframe)
12. [st.plotly_chart](#stplotly_chart)
13. [st.metric](#stmetric)
14. [st.download_button](#stdownload_button)
15. [st.spinner](#stspinner)
16. [st.expander](#stexpander)
17. [st.success / st.warning / st.error / st.info / st.caption](#stsuccess--stwarning--sterror--stinfo--stcaption)
18. [st.session_state](#stsession_state)
19. [@st.cache_resource](#stcache_resource)
20. [Plotly - Graficos interactivos](#plotly---graficos-interactivos)

---

## st.set_page_config

### Proposito
Configura los parametros globales de la pagina: titulo de la pestana, icono, layout y estado inicial de la barra lateral.

### Valor para el usuario
Proporciona identidad visual profesional. El layout `wide` aprovecha pantallas grandes y multiples columnas.

### Ejemplo de codigo
```python
st.set_page_config(
    page_title="Clasificacion Retail | Prediccion Mayorista/Minorista",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

---

## st.markdown

### Proposito
Renderiza HTML y Markdown. Permite inyectar CSS personalizado, crear tarjetas HTML, gradientes y estilos avanzados.

### Valor para el usuario
La interfaz se disena con identidad visual corporativa: tarjetas de resultado coloreadas, KPI cards, gradientes, fuentes Inter de Google Fonts, y barras de confianza.

### Ejemplo de codigo
```python
# Inyectar CSS personalizado
st.markdown("<style> body { background: #f5f5f5; } </style>", unsafe_allow_html=True)

# Tarjeta KPI
st.markdown(f"""
<div class="kpi-card">
    <div class="kpi-value" style="color: #e94560;">{valor}</div>
    <div class="kpi-label">{label}</div>
</div>
""", unsafe_allow_html=True)
```

### Como adaptarlo
- Agregue nuevas reglas CSS en el bloque `<style>` global.
- Las clases disponibles son: `.main-header`, `.result-card`, `.kpi-card`, `.metric-box`, `.section-title`, `.footer`, `.sidebar-info`, `.confidence-badge`.
- Use `unsafe_allow_html=True` solo con contenido controlado.

---

## st.sidebar

### Proposito
Contenedor lateral fijo para navegacion, controles, filtros y configuraciones. Se accede con `st.sidebar.<componente>()`.

### Valor para el usuario
Separa navegacion y controles del area de resultados. La sidebar contiene:
- Selector de modulo (`st.radio`)
- Parametros de entrada (Tab 1)
- Carga de archivos y filtros (Tab 2)
- Controles de analisis (Tabs 3 y 4)
- Info del modelo cargado

### Ejemplo de codigo
```python
pagina = st.sidebar.radio(
    "Seleccione modulo",
    ["Prediccion Individual", "Carga por Lote (CSV)", "Analisis del Modelo", "Escenarios What-If"],
    key="pagina_activa",
)
```

---

## st.radio

### Proposito
Selector de opcion unica con botones de radio. Usado como navegador principal entre modulos y selector de modo What-If.

### Valor para el usuario
Proporciona navegacion clara entre los 4 modulos del dashboard y entre modos del simulador What-If.

### Ejemplo de codigo
```python
modo_whatif = st.sidebar.radio(
    "Seleccione tipo de analisis",
    ["Sliders en Tiempo Real", "Curva de Sensibilidad", "Comparador A/B"],
    key="modo_whatif",
)
```

### Como adaptarlo
- Use `label_visibility="collapsed"` para ocultar la etiqueta y ahorrar espacio.
- Agregue `key="..."` para controlar el estado desde session_state.
- Para multiples opciones, considere `st.selectbox`.

---

## st.number_input

### Proposito
Campo numerico con restricciones de minimo, maximo, paso y formato.

### Valor para el usuario
Garantiza que los valores ingresados esten dentro de rangos validos para el modelo.

### Ejemplo de codigo
```python
cantidad_kg = st.number_input(
    "Cantidad (kg)", min_value=1, max_value=500, value=100, step=1,
    help="Cantidad de producto en kilogramos.",
)
```

---

## st.slider

### Proposito
Control deslizante para seleccionar valores numericos. Tambien usado para ajustar el umbral de decision en tiempo real.

### Valor para el usuario
Experiencia intuitiva para explorar como cambios en los parametros afectan la prediccion.

### Ejemplo de codigo
```python
umbral_confianza = st.slider(
    "Umbral de decision", 0.0, 1.0, 0.5, 0.05,
    help="Ajuste el umbral para reclasificar.",
)
```

---

## st.button

### Proposito
Boton que dispara una accion explicita (clasificar, limpiar).

### Valor para el usuario
Control explicito para ejecutar la prediccion individual. El boton "Limpiar" reinicia el estado.

### Ejemplo de codigo
```python
if st.button("Clasificar Operacion", type="primary", use_container_width=True):
    # Logica de prediccion
    ...
```

---

## st.selectbox

### Proposito
Menu desplegable para seleccionar una opcion de una lista. Usado para elegir datasets de prueba, feature a variar, filtros y frecuencia temporal.

### Valor para el usuario
Permite elegir entre multiples opciones sin ocupar espacio vertical excesivo.

### Ejemplo de codigo
```python
csv_seleccionado = st.sidebar.selectbox(
    "Datos de prueba pre-cargados",
    ["Ninguno (subir archivo propio)"] + ["datos_prueba_50.csv", "datos_prueba_200.csv"],
)

filtro_clase = st.sidebar.selectbox("Filtrar por clase", ["Todas", "Mayorista", "Minorista"])
```

---

## st.file_uploader

### Proposito
Componente de subida de archivos. Permite al usuario cargar un CSV desde su maquina local.

### Valor para el usuario
Permite procesar datos reales de la empresa sin necesidad de modificar el codigo. El modelo clasifica todas las transacciones del archivo.

### Ejemplo de codigo
```python
archivo_subido = st.sidebar.file_uploader(
    "Subir archivo CSV",
    type=["csv"],
    help="El CSV debe contener: cantidad_kg, precio_unitario, descuento_pct",
)
if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
```

### Como adaptarlo
- `type=["csv"]` restringe a archivos CSV.
- Valide las columnas antes de procesar con `validar_csv()`.
- Para multiples archivos, use `accept_multiple_files=True`.

---

## st.columns

### Proposito
Layout de columnas para organizar contenido horizontalmente. Usado extensivamente para KPIs, graficos lado a lado y comparador A/B.

### Valor para el usuario
Maximiza la densidad de informacion aprovechando el layout wide.

### Ejemplo de codigo
```python
cols_kpi = st.columns(6)
for i, (valor, label, color) in enumerate(kpis):
    with cols_kpi[i]:
        st.markdown(f"""<div class="kpi-card">...</div>""", unsafe_allow_html=True)

col_graf1, col_graf2 = st.columns([1, 1])
with col_graf1:
    st.plotly_chart(fig_donut, use_container_width=True)
with col_graf2:
    st.plotly_chart(fig_hist, use_container_width=True)
```

### Como adaptarlo
- `st.columns([2, 1])` crea columnas proporcionales.
- `st.columns(6)` para dashboards de KPIs.

---

## st.dataframe

### Proposito
Renderiza un DataFrame de pandas como tabla interactiva con ordenamiento, busqueda y estilos condicionales.

### Valor para el usuario
Muestra los resultados del procesamiento batch con formato condicional: filas rojas para Mayorista, azules para Minorista. Permite inspeccionar y filtrar datos.

### Ejemplo de codigo
```python
def color_filas(row):
    if row.get("clase_nombre") == "Mayorista":
        return ["background-color: #fef2f2" for _ in row.index]
    return ["background-color: #f8faff" for _ in row.index]

st.dataframe(
    df_mostrar.style.format({"prob_mayorista": "{:.1%}"}).apply(color_filas, axis=1),
    use_container_width=True, height=400,
)
```

### Como adaptarlo
- `.style.format()` formatea columnas numericas.
- `.style.apply()` aplica estilos condicionales por fila o celda.
- `height=400` limita la altura con scroll.

---

## st.plotly_chart

### Proposito
Renderiza graficos interactivos de la libreria Plotly. Es el componente principal para todas las visualizaciones del dashboard v2.

### Valor para el usuario
Graficos profesionales con tooltips, zoom, pan, descarga como PNG, y interactividad completa. Reemplaza a `st.bar_chart` nativo.

### Ejemplo de codigo
```python
import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=85,
    gauge={"axis": {"range": [0, 100]}},
))
st.plotly_chart(fig, use_container_width=True)
```

### Graficos implementados con Plotly

| Grafico | Tipo Plotly | Ubicacion |
|---------|-------------|-----------|
| Gauge de confianza | `go.Indicator` (gauge) | Tab 1, Tab 4 |
| Barras de probabilidades | `go.Bar` (horizontal) | Tab 1, Tab 4 |
| Feature importance | `go.Bar` (horizontal, colorscale) | Tab 3 |
| Waterfall contribucion | `go.Bar` (horizontal, coloreado) | Tab 1, Tab 4 |
| Donut de clases | `go.Pie` (hole=0.55) | Tab 2 |
| Histograma de probs | `px.histogram` | Tab 2 |
| Serie temporal | `go.Scatter` (dual Y-axis) | Tab 2 |
| Barras apiladas confianza | `go.Bar` (stacked, horizontal) | Tab 2 |
| Superficie de decision | `go.Heatmap` + `go.Contour` | Tab 3 |
| Matriz de confusion | `px.imshow` | Tab 3 |
| Curva ROC | `go.Scatter` | Tab 3 |
| Curva de sensibilidad | `go.Scatter` | Tab 4 |
| Comparador A/B | `go.Bar` (grouped) | Tab 4 |

### Como adaptarlo
- `use_container_width=True` expande el grafico al ancho del contenedor.
- Agregue `key="..."` para evitar conflictos de IDs de Plotly.
- Consulte la seccion [Plotly - Graficos interactivos](#plotly---graficos-interactivos) para mas detalles.

---

## st.metric

### Proposito
Muestra una metrica numerica con etiqueta, valor y delta.

### Valor para el usuario
Usado para mostrar conteos de alta confianza en la seccion de exportacion del Tab 2.

### Ejemplo de codigo
```python
st.metric("Mayoristas alta confianza", n_may_alta)
st.metric("Minoristas alta confianza", n_min_alta)
```

---

## st.download_button

### Proposito
Boton que permite al usuario descargar datos como archivo. Usado para exportar resultados batch a CSV.

### Valor para el usuario
Permite llevarse los resultados del procesamiento para analisis externo o integracion con otros sistemas.

### Ejemplo de codigo
```python
csv_export = df_resultados.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Descargar resultados completos (CSV)",
    data=csv_export,
    file_name="predicciones_retail_20260101.csv",
    mime="text/csv",
)
```

### Como adaptarlo
- `mime="text/csv"` para archivos CSV.
- `mime="application/json"` para JSON.
- Use `help="..."` para tooltips.

---

## st.spinner

### Proposito
Muestra un indicador de carga animado mientras se ejecuta una operacion larga.

### Valor para el usuario
Proporciona feedback visual durante el procesamiento batch, evitando que el usuario piense que la app se congelo.

### Ejemplo de codigo
```python
with st.spinner("Procesando transacciones..."):
    predicciones = modelo.predict(X_batch)
    probabilidades = modelo.predict_proba(X_batch)
```

---

## st.expander

### Proposito
Contenedor colapsable para contenido secundario. Usado para datos de entrada, recomendaciones accionables y reporte de clasificacion detallado.

### Valor para el usuario
Mantiene la interfaz limpia ocultando detalles tecnicos o informacion complementaria que no todos los usuarios necesitan ver.

### Ejemplo de codigo
```python
with st.expander("Ver datos de entrada y recomendaciones"):
    st.dataframe(df_entrada)
    st.markdown("#### Acciones recomendadas")
    for rec in recomendaciones:
        st.markdown(f"- {rec}")
```

---

## st.success / st.warning / st.error / st.info / st.caption

### Proposito
Mensajes estilizados con colores semanticos.

| Componente | Color | Uso en el dashboard |
|------------|-------|---------------------|
| `st.success` | Verde | Predicciones Mayorista de alta/media confianza |
| `st.info` | Azul | Predicciones Minorista, instrucciones, datos faltantes |
| `st.warning` | Amarillo | Advertencias de validacion |
| `st.error` | Rojo | Errores de carga de modelo, excepciones |
| `st.caption` | Gris | Texto explicativo secundario debajo de graficos |

### Ejemplo de codigo
```python
st.success("Alta confianza en cliente Mayorista (96%).")
st.caption("Las barras rojas indican que la variable favorece Mayorista.")
```

---

## st.session_state

### Proposito
Diccionario que persiste valores entre rerenders de Streamlit.

### Valor para el usuario
Mantiene el estado de predicciones, resultados batch y navegacion entre modulos sin perder datos al interactuar con widgets.

### Variables de session_state utilizadas

| Variable | Tipo | Proposito |
|----------|------|-----------|
| `pagina_activa` | str | Modulo de navegacion activo |
| `prediccion_individual` | bool | Si hay una prediccion individual realizada |
| `clase_predicha` | int | Clase predicha (0 o 1) |
| `prob_mayorista` | float | Probabilidad de Mayorista |
| `prob_minorista` | float | Probabilidad de Minorista |
| `etiqueta_clase` | str | "Mayorista" o "Minorista" |
| `df_entrada` | DataFrame | Datos de entrada de la prediccion individual |
| `resultados_batch` | DataFrame | Resultados del procesamiento batch |
| `df_batch_original` | DataFrame | Datos originales cargados del CSV |

### Ejemplo de codigo
```python
if "prediccion_individual" not in st.session_state:
    st.session_state.prediccion_individual = False

st.session_state.clase_predicha = int(clase_predicha)
st.session_state.prob_mayorista = probabilidades[1]
```

---

## @st.cache_resource

### Proposito
Cachea el modelo ML en memoria para no recargarlo en cada interaccion.

### Valor para el usuario
Reduce el tiempo de carga drasticamente: el modelo .pkl se carga una sola vez al iniciar la app.

### Ejemplo de codigo
```python
@st.cache_resource
def cargar_modelo(ruta_modelo: str):
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(f"No se encontro el modelo en: {ruta_modelo}")
    return joblib.load(ruta_modelo)

modelo = cargar_modelo("modelo_clasificacion_retail.pkl")
```

---

## Plotly - Graficos interactivos

### Proposito
Libreria de visualizacion que genera graficos interactivos (zoom, pan, tooltips, descarga). Se integra con Streamlit via `st.plotly_chart()`.

### Librerias utilizadas

```python
import plotly.graph_objects as go    # Graficos de bajo nivel (gauge, heatmap, scatter personalizado)
import plotly.express as px          # Graficos de alto nivel (histogram, imshow)
from plotly.subplots import make_subplots  # Subplots con ejes duales
```

### Patrones comunes

#### Gauge (velocimetro de confianza)
```python
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=85,
    number={"suffix": "%", "font": {"size": 36}},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#10b981"},
        "steps": [
            {"range": [0, 70], "color": "#fee2e2"},
            {"range": [70, 90], "color": "#fef3c7"},
            {"range": [90, 100], "color": "#d1fae5"},
        ],
    },
))
fig.update_layout(height=250, margin=dict(t=30, b=10, l=20, r=20))
st.plotly_chart(fig, use_container_width=True)
```

#### Barras horizontales con colores condicionales
```python
fig = go.Figure(go.Bar(
    x=valores, y=etiquetas, orientation="h",
    marker_color=colores,
    text=[f"{v:.1f}%" for v in valores],
    textposition="outside",
))
```

#### Donut chart
```python
fig = go.Figure(go.Pie(
    labels=["Mayorista", "Minorista"],
    values=[n_may, n_min],
    hole=0.55,
    marker_colors=["#e94560", "#3b82f6"],
))
```

#### Heatmap
```python
fig = go.Figure(go.Heatmap(
    x=kg_range, y=precio_range, z=Z,
    colorscale=[[0, "#3b82f6"], [0.5, "#a78bfa"], [1, "#e94560"]],
    colorbar=dict(title="P(Mayorista)"),
))
```

#### Linea con area
```python
fig = go.Figure(go.Scatter(
    x=fechas, y=valores, mode="lines+markers",
    line=dict(color="#e94560", width=2.5),
    fill="tozeroy", fillcolor="rgba(233,69,96,0.1)",
))
```

#### Subplots con doble eje Y
```python
from plotly.subplots import make_subplots
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=fechas, y=pct_may, name="% Mayorista"), secondary_y=False)
fig.add_trace(go.Scatter(x=fechas, y=total, name="Transacciones"), secondary_y=True)
```

### Paleta de colores del dashboard

| Color | Hex | Uso |
|-------|-----|-----|
| Rojo Mayorista | `#e94560` | Clase Mayorista, barras positivas, acentos |
| Azul Minorista | `#3b82f6` | Clase Minorista, barras negativas |
| Verde exito | `#10b981` | Alta confianza, metricas positivas |
| Ambar warning | `#f59e0b` | Confianza media |
| Rojo peligro | `#ef4444` | Baja confianza, errores |
| Purpura KPIs | `#6366f1` | Transacciones totales, acentos neutros |
| Gris texto | `#64748b` | Texto secundario, labels |
| Fondo oscuro | `#0f172a` | Header, gradientes |

### Como adaptarlo
- Modifique `colorscale` en heatmaps para cambiar el esquema de color.
- Use `update_layout(height=..., margin=...)` para ajustar dimensiones.
- `hovertemplate` permite personalizar tooltips con formato HTML.
- Agregue `key="..."` a `st.plotly_chart()` si renderiza el mismo grafico multiples veces en diferentes tabs.

---

## Resumen de buenas practicas

| Practica | Descripcion |
|---|---|
| Cacheo del modelo | `@st.cache_resource` para cargar el .pkl una sola vez |
| Validacion de entradas | `min_value`/`max_value` en inputs y sliders; validar columnas de CSV |
| Nombres de columnas | DataFrame con los nombres exactos de `feature_names_in_` |
| Separacion de logica | Funciones independientes para graficos, prediccion e interpretacion |
| Manejo de errores | Try/except en carga de modelo, prediccion y procesamiento batch |
| Persistencia de estado | `st.session_state` para mantener resultados entre modulos |
| Layout responsive | `st.columns` con `use_container_width=True` en graficos |
| Plotly interactivo | `go.Figure` con tooltips, colores semanticos y temas consistentes |
| Exportacion | `st.download_button` para CSV de resultados |
| Feedback visual | `st.spinner` durante operaciones largas, `st.toast` para notificaciones |
| Seguridad | No cargar .pkl de fuentes no confiables; contenido HTML solo controlado |
