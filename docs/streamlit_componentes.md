# Documentacion de Componentes Streamlit Utilizados

Guia tecnica de cada componente de Streamlit implementado en el dashboard de Clasificacion Retail. Cada seccion explica el proposito, valor para el usuario, ejemplo de codigo y como adaptarlo.

---

## Tabla de Contenidos

1. [st.set_page_config](#stset_page_config)
2. [st.markdown](#stmarkdown)
3. [st.title / st.header / st.subheader](#sttitle--stheader--stsubheader)
4. [st.sidebar](#stsidebar)
5. [st.number_input](#stnumber_input)
6. [st.slider](#stslider)
7. [st.button](#stbutton)
8. [st.metric](#stmetric)
9. [st.columns](#stcolumns)
10. [st.dataframe](#stdataframe)
11. [st.bar_chart](#stbar_chart)
12. [st.success / st.warning / st.error / st.info](#stsuccess--stwarning--sterror--stinfo)
13. [st.expander](#stexpander)
14. [st.session_state](#stsession_state)
15. [@st.cache_resource](#stcache_resource)

---

## st.set_page_config

### Proposito
Configura los parametros globales de la pagina: titulo de la pestana, icono (favicon), layout y estado inicial de la barra lateral.

### Valor para el usuario
Proporciona una identidad visual profesional desde el momento en que se abre la pestana del navegador. El layout `wide` aprovecha mejor pantallas grandes.

### Ejemplo de codigo
```python
st.set_page_config(
    page_title="Clasificacion Retail | Prediccion Mayorista/Minorista",
    page_icon="img.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

### Como adaptarlo
- Cambie `page_title` para modificar el texto de la pestana.
- Use `layout="centered"` si prefiere un diseno mas estrecho.
- Consulte [emojis Unicode](https://unicode.org/emoji/charts/full-emoji-list.html) para `page_icon`.

---

## st.markdown

### Proposito
Renderiza contenido HTML y Markdown. Es el componente principal para inyectar CSS personalizado, estructuras HTML complejas y texto formateado.

### Valor para el usuario
Permite disenar una interfaz visualmente atractiva que va mas alla de los limites del diseno predeterminado de Streamlit, incluyendo tarjetas, gradientes y estilos personalizados.

### Ejemplo de codigo
```python
# Inyectar CSS personalizado
st.markdown("<style> body { background: #f5f5f5; } </style>", unsafe_allow_html=True)

# HTML con clases CSS personalizadas
st.markdown("""
<div class="result-card mayorista">
    <div class="prediction-label">MAYORISTA</div>
</div>
""", unsafe_allow_html=True)
```

### Como adaptarlo
- Agregue nuevas reglas CSS en el bloque `<style>` para personalizar colores, fuentes o animaciones.
- Use `unsafe_allow_html=True` solo cuando controle el contenido HTML (evite inyectar input del usuario directamente).

---

## st.sidebar

### Proposito
Contenedor lateral fijo para alojar controles de entrada, filtros y configuraciones. Se accede mediante `st.sidebar.<componente>()`.

### Valor para el usuario
Separa claramente los controles de entrada del area de resultados. La sidebar siempre visible facilita iterar sobre diferentes configuraciones sin perder de vista los resultados.

### Ejemplo de codigo
```python
st.sidebar.markdown("## Parametros de Entrada")
cantidad = st.sidebar.number_input("Cantidad (kg)", min_value=1, max_value=500)
```

### Como adaptarlo
- Use `st.sidebar.selectbox` para agregar opciones categoricas adicionales.
- Si la sidebar se vuelve muy larga, considere usar `st.expander` dentro de ella.

---

## st.number_input

### Proposito
Campo numerico interactivo que permite al usuario introducir valores con restricciones de minimo, maximo, paso y formato.

### Valor para el usuario
Garantiza que los valores ingresados esten dentro de rangos validos, previniendo errores en el modelo. El formato de visualizacion mejora la legibilidad.

### Ejemplo de codigo
```python
cantidad_kg = st.number_input(
    "Cantidad (kg)",
    min_value=1,
    max_value=500,
    value=100,
    step=1,
    help="Cantidad de producto en kilogramos. Rango permitido: 1 - 500 kg.",
)
```

### Como adaptarlo
- Ajuste `min_value` y `max_value` segun los rangos validos de su modelo.
- Use `format="%.2f"` para valores decimales con dos decimales.
- Agregue `help="..."` para mostrar tooltips informativos.

---

## st.slider

### Proposito
Control deslizante para seleccionar valores numericos dentro de un rango definido.

### Valor para el usuario
Ofrece una experiencia mas intuitiva que `number_input` para valores porcentuales o rangos continuos. El usuario puede explorar rapidamente como cambia la prediccion al mover el slider.

### Ejemplo de codigo
```python
descuento_pct = st.slider(
    "Descuento (%)",
    min_value=0,
    max_value=100,
    value=10,
    step=1,
    help="Porcentaje de descuento aplicado a la operacion.",
)
```

### Como adaptarlo
- Para valores flotantes, use `step=0.5` o similar.
- Para variables categoricas ordinales, considere `st.select_slider`.

---

## st.button

### Proposito
Boton que dispara una accion cuando el usuario hace clic. En este proyecto, activa el proceso de clasificacion.

### Valor para el usuario
Proporciona un control explicito para ejecutar la prediccion. El usuario puede ajustar todos los parametros antes de lanzar la clasificacion, evitando recalculaciones innecesarias.

### Ejemplo de codigo
```python
boton_clasificar = st.button(
    "Clasificar Operacion",
    type="primary",
    use_container_width=True,
)

if boton_clasificar:
    # Logica de prediccion
    ...
```

### Como adaptarlo
- Use `type="secondary"` para botones menos destacados.
- `use_container_width=True` hace que el boton ocupe todo el ancho disponible.
- Para flujos mas reactivos, puede eliminar el boton y usar widgets con callback `on_change`.

---

## st.metric

### Proposito
Muestra una metrica numerica con etiqueta, valor y delta (cambio respecto a referencia). Alternativamente, en este proyecto se usa HTML personalizado con clases CSS para mayor control visual.

### Valor para el usuario
Comunica rapidamente valores clave (probabilidades, importes) en un formato visualmente destacado y facil de escanear.

### Ejemplo de codigo (version nativa)
```python
st.metric(
    label="Probabilidad Mayorista",
    value=f"{prob_may:.1%}",
    delta=None,
)
```

### Como adaptarlo
- Use `delta` para mostrar cambios respecto a un valor anterior (ej. variacion de precio).
- `delta_color="inverse"` invierte la logica de colores (rojo = negativo, verde = positivo).

---

## st.columns

### Proposito
Crea un layout de columnas para organizar contenido horizontalmente.

### Valor para el usuario
Permite mostrar multiples metricas o graficos uno al lado del otro, aprovechando el espacio horizontal y mejorando la densidad de informacion.

### Ejemplo de codigo
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("...")  # Contenido de la columna 1

with col2:
    st.markdown("...")  # Contenido de la columna 2

with col3:
    st.markdown("...")  # Contenido de la columna 3
```

### Como adaptarlo
- Use `st.columns([2, 1])` para crear columnas de ancho proporcional (la primera ocupa 2/3).
- Anide `st.columns` dentro de otras columnas para layouts mas complejos.
- Para responsive design, Streamlit adapta automaticamente las columnas en pantallas pequenas.

---

## st.dataframe

### Proposito
Renderiza un DataFrame de pandas como tabla interactiva con ordenamiento y busqueda.

### Valor para el usuario
Permite al usuario inspeccionar los datos exactos que se enviaron al modelo, aportando transparencia y facilitando la depuracion.

### Ejemplo de codigo
```python
st.dataframe(df_entrada, use_container_width=True)
```

### Como adaptarlo
- Use `st.dataframe(df, column_config={...})` para personalizar formato de columnas.
- `use_container_width=True` expande la tabla al ancho disponible.
- Para tablas estaticas, use `st.table(df)`.

---

## st.bar_chart

### Proposito
Genera un grafico de barras nativo de Streamlit a partir de un DataFrame.

### Valor para el usuario
Visualiza rapidamente las probabilidades relativas de cada clase, facilitando la comprension de la confianza del modelo.

### Ejemplo de codigo
```python
df_prob = pd.DataFrame({
    "Clase": ["Mayorista", "Minorista"],
    "Probabilidad": [0.96, 0.04],
})
st.bar_chart(df_prob.set_index("Clase"), use_container_width=True)
```

### Como adaptarlo
- Para graficos mas complejos, use `st.pyplot` (matplotlib) o `st.plotly_chart` (Plotly interactivo).
- Cambie el color con `color="#e94560"`.
- Use `st.area_chart` o `st.line_chart` para tendencias temporales.

---

## st.success / st.warning / st.error / st.info

### Proposito
Muestran mensajes estilizados con iconos y colores semanticos para comunicar exito, advertencia, error o informacion.

### Valor para el usuario
Proporcionan retroalimentacion inmediata y contextual sobre el resultado de la prediccion, con codificacion visual clara.

### Ejemplo de codigo
```python
st.success("Alta confianza en cliente Mayorista (96%).")
st.info("Confianza moderada en cliente Minorista (78%).")
st.warning("La prediccion tiene baja confianza. Considere verificacion adicional.")
st.error("No se pudo cargar el modelo. Verifique la ruta del archivo .pkl.")
```

### Como adaptarlo
- Use `st.success` para predicciones de alta confianza.
- Use `st.info` para predicciones de confianza moderada-baja.
- Use `st.error` solo para errores tecnicos (modelo no cargado, excepciones).
- Combine con `st.markdown()` dentro del mensaje para texto enriquecido (negritas, iconos).

---

## st.expander

### Proposito
Contenedor colapsable que oculta/muestra contenido secundario bajo demanda.

### Valor para el usuario
Mantiene la interfaz limpia al ocultar informacion complementaria (datos tecnicos, documentacion, datos de entrada del modelo) que no todos los usuarios necesitan ver.

### Ejemplo de codigo
```python
with st.expander("Ver datos de entrada enviados al modelo"):
    st.dataframe(df_entrada)
```

### Como adaptarlo
- `expanded=True` muestra el contenido por defecto.
- Use `expander` para documentacion inline, logs de debug o configuraciones avanzadas.

---

## st.session_state

### Proposito
Diccionario global que persiste valores entre rerenders de Streamlit, permitiendo mantener estado sin recargar toda la pagina.

### Valor para el usuario
Evita que los resultados de la prediccion desaparezcan si el usuario interactua con otro widget. Permite que la prediccion persista hasta que se haga una nueva.

### Ejemplo de codigo
```python
if "prediccion_realizada" not in st.session_state:
    st.session_state.prediccion_realizada = False

# Almacenar resultados
st.session_state.clase_predicha = int(clase_predicha)
st.session_state.prob_mayorista = probabilidades[1]

# Recuperar resultados
etiqueta = st.session_state.etiqueta_clase
```

### Como adaptarlo
- Inicialice todas las claves de session_state al principio de la app.
- Use `st.session_state.clear()` para reiniciar el estado (util en un boton de "Reset").
- Para widgets con estado automatico, use el parametro `key="..."`.

---

## @st.cache_resource

### Proposito
Decorador que cachea el resultado de una funcion a nivel de recurso. Ideal para objetos pesados que no deben recargarse (modelos ML, conexiones a bases de datos).

### Valor para el usuario
Reduce drasticamente el tiempo de carga: el modelo se carga en memoria una sola vez, no en cada interaccion del usuario con la app.

### Ejemplo de codigo
```python
@st.cache_resource
def cargar_modelo(ruta_modelo: str):
    return joblib.load(ruta_modelo)

modelo = cargar_modelo("modelo_clasificacion_retail.pkl")
```

### Como adaptarlo
- Use `@st.cache_resource` para objetos no serializables o que no deben duplicarse.
- Para datos tabulares, use `@st.cache_data` en su lugar.
- Agregue `ttl=3600` para invalidar el cache despues de un tiempo (en segundos).
- `show_spinner=True` muestra un indicador de carga mientras se ejecuta la funcion.

---

## Resumen de buenas practicas

| Practica | Descripcion |
|---|---|
| Cacheo del modelo | Usar `@st.cache_resource` para cargar el .pkl una sola vez |
| Validacion de entradas | Definir `min_value`/`max_value` en inputs y sliders |
| Nombres de columnas | Construir DataFrame con los nombres exactos de `feature_names_in_` |
| Separacion de logica | Funciones independientes para carga, prediccion y visualizacion |
| Manejo de errores | Capturar excepciones al cargar el modelo y mostrar `st.error` |
| Persistencia de estado | Usar `st.session_state` para mantener resultados visibles |
| Seguridad | No cargar .pkl de fuentes no confiables; el modelo es fijo |
| HTML seguro | Usar `unsafe_allow_html=True` solo con contenido controlado |
