"""
Dashboard de Clasificacion Retail - Prediccion de Clientes Mayoristas vs Minoristas
-----------------------------------------------------------------------
Aplicacion Streamlit que carga un modelo RandomForest entrenado (.pkl)
y permite realizar predicciones dinamicas de clasificacion retail.

Modelo inspeccionado:
  - Tipo: RandomForestClassifier (scikit-learn)
  - Features: cantidad_kg, precio_unitario, descuento_pct
  - Clases: [0 = Minorista, 1 = Mayorista]
  - Soporta predict_proba: Si
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Configuracion de la pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Clasificacion Retail | Prediccion Mayorista/Minorista",
    page_icon="img.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS personalizado para diseno moderno
# ---------------------------------------------------------------------------
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #e94560;
        letter-spacing: -0.5px;
    }

    .main-header p {
        font-size: 1.1rem;
        color: #a8b2d1;
        margin: 0;
    }

    .result-card {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }

    .result-card.mayorista {
        background: linear-gradient(145deg, #fff5f5, #ffe0e0);
        border: 2px solid #e94560;
    }

    .result-card.minorista {
        background: linear-gradient(145deg, #f0f9ff, #dbeafe);
        border: 2px solid #3b82f6;
    }

    .prediction-label {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        letter-spacing: -1px;
    }

    .prediction-label.mayorista {
        color: #e94560;
    }

    .prediction-label.minorista {
        color: #3b82f6;
    }

    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s;
    }

    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    .metric-box .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }

    .metric-box .label {
        font-size: 0.85rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e94560;
        display: inline-block;
    }

    .footer {
        text-align: center;
        padding: 2rem;
        color: #9ca3af;
        font-size: 0.85rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #e94560, #c23152);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .sidebar-info {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #6b7280;
        border-left: 3px solid #e94560;
    }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Carga del modelo (cacheado para rendimiento)
# ---------------------------------------------------------------------------


@st.cache_resource
def cargar_modelo(ruta_modelo: str):
    """
    Carga el modelo RandomForest desde un archivo .pkl usando joblib.

    Args:
        ruta_modelo: Ruta relativa o absoluta al archivo .pkl

    Returns:
        modelo: instancia de RandomForestClassifier

    Raises:
        FileNotFoundError: si el archivo .pkl no existe
        Exception: cualquier otro error de carga
    """
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(
            f"No se encontro el archivo del modelo en: {ruta_modelo}\n"
            "Asegurese de colocar 'modelo_clasificacion_retail.pkl' en la raiz del proyecto."
        )
    modelo = joblib.load(ruta_modelo)
    return modelo


# ---------------------------------------------------------------------------
# Constantes del modelo (extraidas en tiempo de inspeccion)
# ---------------------------------------------------------------------------
RUTA_MODELO = "modelo_clasificacion_retail.pkl"

# Nombres de columnas esperados por el modelo, en el orden exacto de fitting
# Si cambia el modelo, actualizar estos valores segun feature_names_in_
COLUMNAS_MODELO = ["cantidad_kg", "precio_unitario", "descuento_pct"]

# Mapeo de clases detectado durante la inspeccion del modelo
# Clase 0 -> Minorista, Clase 1 -> Mayorista
MAPA_CLASES = {0: "Minorista", 1: "Mayorista"}

# ---------------------------------------------------------------------------
# Carga del modelo con manejo de errores
# ---------------------------------------------------------------------------
try:
    modelo = cargar_modelo(RUTA_MODELO)
    modelo_cargado = True
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    modelo_cargado = False
except Exception as e:
    st.error(f"Error inesperado al cargar el modelo: {e}")
    modelo_cargado = False

# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------


def construir_dataframe(cantidad_kg: float, precio_unitario: float, descuento_pct: float) -> pd.DataFrame:
    """
    Construye un DataFrame de entrada con los nombres de columna exactos
    que espera el modelo.

    Args:
        cantidad_kg: Cantidad en kilogramos (1-500)
        precio_unitario: Precio por unidad
        descuento_pct: Porcentaje de descuento (0-100)

    Returns:
        DataFrame con una fila y las columnas requeridas por el modelo
    """
    return pd.DataFrame(
        [[cantidad_kg, precio_unitario, descuento_pct]],
        columns=COLUMNAS_MODELO,
    )


def obtener_interpretacion(clase_predicha: int, probabilidad: float) -> str:
    """
    Genera un mensaje interpretativo segun la clasificacion y su confianza.

    Args:
        clase_predicha: Clase predicha (0 = Minorista, 1 = Mayorista)
        probabilidad: Probabilidad de la clase predicha (0.0 - 1.0)

    Returns:
        Mensaje interpretativo en lenguaje de negocio
    """
    etiqueta = MAPA_CLASES[clase_predicha]

    if clase_predicha == 1:
        if probabilidad >= 0.9:
            return (
                f"Alta confianza en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "El volumen de compra y el descuento aplicado son indicativos de un perfil mayorista tipico. "
                "Se recomienda aplicar condiciones comerciales para cliente mayorista."
            )
        elif probabilidad >= 0.7:
            return (
                f"Confianza moderada-alta en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "La operacion se inclina hacia un perfil mayorista, aunque no de forma concluyente. "
                "Considere verificar el historial del cliente."
            )
        else:
            return (
                f"Confianza baja en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "La prediccion favorece Mayorista por margen estrecho. "
                "Se sugiere analisis adicional antes de aplicar tarifas mayoristas."
            )
    else:
        if probabilidad >= 0.9:
            return (
                f"Alta confianza en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "El bajo volumen o el perfil de compra indican un cliente minorista tipico. "
                "Se recomienda aplicar precios de venta al publico."
            )
        elif probabilidad >= 0.7:
            return (
                f"Confianza moderada-alta en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "La operacion probablemente corresponde a un cliente minorista. "
                "Mantenga las condiciones estandar de venta minorista."
            )
        else:
            return (
                f"Confianza baja en cliente **{etiqueta}** ({probabilidad:.0%}). "
                "La prediccion favorece Minorista por margen estrecho. "
                "Revise si el cliente podria calificar para condiciones especiales."
            )


# ---------------------------------------------------------------------------
# Cabecera principal
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="main-header">
    <h1>Clasificador Retail Inteligente</h1>
    <p>Prediccion dinamica de perfil de cliente: Mayorista vs Minorista</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Descripcion del proposito
# ---------------------------------------------------------------------------
with st.expander("Acerca de esta aplicacion", expanded=False):
    st.markdown(
        """
    ### Que hace esta aplicacion?
    Esta herramienta utiliza un modelo de Machine Learning (Random Forest) entrenado con datos sinteticos
    de retail para clasificar automaticamente si una operacion de compra corresponde a un perfil de
    **cliente Mayorista** o **cliente Minorista**.

    ### Como funciona?
    1. Introduzca los datos de la operacion en la barra lateral izquierda.
    2. El modelo analiza las variables: **cantidad (kg)**, **precio unitario** y **porcentaje de descuento**.
    3. La aplicacion muestra la clasificacion predicha y la probabilidad asociada.
    4. Se genera una interpretacion en lenguaje de negocio para facilitar la toma de decisiones.

    ### Regla de negocio integrada
    El modelo ha aprendido que operaciones con **alto volumen** (ej. >300 kg) y **descuentos significativos**
    tienden a clasificarse como **Mayorista**, mientras que compras de bajo volumen con poco descuento
    corresponden a **Minorista**.
    """
    )

# ---------------------------------------------------------------------------
# Sidebar - Controles de entrada
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    """
<div style="text-align: center; padding-bottom: 1rem;">
    <h2 style="color: #e94560; margin: 0;">Parametros de Entrada</h2>
    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">Ajuste los valores y presione <b>Clasificar</b></p>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

# Input: cantidad_kg
cantidad_kg = st.sidebar.number_input(
    "Cantidad (kg)",
    min_value=1,
    max_value=500,
    value=100,
    step=1,
    help="Cantidad de producto en kilogramos. Rango permitido: 1 - 500 kg.",
)

# Input: precio_unitario
precio_unitario = st.sidebar.number_input(
    "Precio Unitario ($)",
    min_value=0.01,
    max_value=500.0,
    value=10.0,
    step=0.5,
    format="%.2f",
    help="Precio por unidad en la moneda local. Ejemplo: 10.50",
)

# Input: descuento_pct
descuento_pct = st.sidebar.slider(
    "Descuento (%)",
    min_value=0,
    max_value=100,
    value=10,
    step=1,
    help="Porcentaje de descuento aplicado a la operacion. Rango: 0% - 100%.",
)

st.sidebar.markdown("---")

# Boton de clasificacion
boton_clasificar = st.sidebar.button("Clasificar Operacion", type="primary", use_container_width=True)

# Info sobre el modelo en sidebar
st.sidebar.markdown(
    f"""
<div class="sidebar-info">
    <strong>Modelo cargado:</strong> RandomForestClassifier<br>
    <strong>Variables:</strong> {', '.join(COLUMNAS_MODELO)}<br>
    <strong>Clases:</strong> Minorista (0), Mayorista (1)<br>
    <strong>Probabilidades:</strong> Disponible
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Panel principal - Visualizacion de resultados
# ---------------------------------------------------------------------------

# Inicializar variables de sesion
if "prediccion_realizada" not in st.session_state:
    st.session_state.prediccion_realizada = False

# Realizar prediccion al hacer clic
if boton_clasificar:
    if not modelo_cargado:
        st.error("No se puede realizar la prediccion porque el modelo no se cargo correctamente.")
    else:
        try:
            # Construir DataFrame respetando nombres de columnas exactos
            df_entrada = construir_dataframe(cantidad_kg, precio_unitario, descuento_pct)

            # Generar predicciones
            clase_predicha = modelo.predict(df_entrada)[0]
            probabilidades = modelo.predict_proba(df_entrada)[0]

            # Almacenar en session_state para persistencia
            st.session_state.prediccion_realizada = True
            st.session_state.clase_predicha = int(clase_predicha)
            st.session_state.probabilidades = probabilidades
            st.session_state.etiqueta_clase = MAPA_CLASES.get(int(clase_predicha), f"Clase {clase_predicha}")
            st.session_state.prob_mayorista = probabilidades[1]
            st.session_state.prob_minorista = probabilidades[0]
            st.session_state.df_entrada = df_entrada

        except Exception as e:
            st.error(f"Error al generar la prediccion: {e}")
            modelo_cargado = False

# Mostrar resultados si hay una prediccion realizada
if st.session_state.prediccion_realizada:
    st.markdown('<p class="section-title">Resultado de la Clasificacion</p>', unsafe_allow_html=True)

    etiqueta = st.session_state.etiqueta_clase
    prob_may = st.session_state.prob_mayorista
    prob_min = st.session_state.prob_minorista
    clase = st.session_state.clase_predicha

    # --- Fila 1: Tarjeta de resultado principal ---
    css_clase = "mayorista" if clase == 1 else "minorista"
    icono = "img.png" if clase == 1 else "img.png"
    texto_etiqueta = "MAYORISTA" if clase == 1 else "MINORISTA"

    st.markdown(
        f"""
    <div class="result-card {css_clase}">
        <div style="font-size: 0.9rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px;">
            Clasificacion
        </div>
        <div class="prediction-label {css_clase}">{texto_etiqueta}</div>
        <div style="font-size: 1rem; color: #6b7280;">
            Confianza del modelo: <strong>{prob_may if clase == 1 else prob_min:.1%}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # --- Fila 2: Metricas en columnas ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="metric-box">
            <div class="value">{prob_may:.1%}</div>
            <div class="label">Probabilidad Mayorista</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-box">
            <div class="value">{prob_min:.1%}</div>
            <div class="label">Probabilidad Minorista</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        importe_total = cantidad_kg * precio_unitario * (1 - descuento_pct / 100)
        st.markdown(
            f"""
        <div class="metric-box">
            <div class="value">${importe_total:,.2f}</div>
            <div class="label">Importe Total Estimado</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # --- Fila 3: Grafico de probabilidades ---
    st.markdown('<p class="section-title">Probabilidades por Clase</p>', unsafe_allow_html=True)

    df_prob = pd.DataFrame(
        {
            "Clase": ["Mayorista", "Minorista"],
            "Probabilidad": [prob_may, prob_min],
        }
    )

    col_chart, col_interp = st.columns([1, 1])

    with col_chart:
        st.bar_chart(df_prob.set_index("Clase"), use_container_width=True)

    with col_interp:
        st.markdown("### Interpretacion del modelo")
        mensaje = obtener_interpretacion(clase, prob_may if clase == 1 else prob_min)
        if clase == 1:
            st.success(mensaje)
        else:
            st.info(mensaje)

    # --- Fila 4: Datos de entrada (debug / transparencia) ---
    with st.expander("Ver datos de entrada enviados al modelo"):
        st.dataframe(st.session_state.df_entrada, use_container_width=True)
        st.caption(
            "Estos son los valores exactos que recibe el modelo. Las columnas y el orden deben coincidir "
            "con las variables usadas durante el entrenamiento."
        )

elif not st.session_state.prediccion_realizada:
    # Estado inicial: placeholder con instrucciones
    st.markdown(
        """
    <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">img.png</div>
        <h3 style="color: #374151; margin-bottom: 0.5rem;">Ajuste los parametros y presione <b>Clasificar Operacion</b></h3>
        <p style="font-size: 0.95rem;">
            Use la barra lateral para configurar los valores de la operacion.
            El modelo clasificara automaticamente el perfil del cliente.
        </p>
        <div style="margin-top: 2rem; padding: 1rem; background: #f9fafb; border-radius: 8px; display: inline-block; text-align: left;">
            <strong>Sugerencia rapida:</strong><br>
            Pruebe con: cantidad = <b>400 kg</b>, precio = <b>$10</b>, descuento = <b>15%</b><br>
            Resultado esperado: <span style="color: #e94560; font-weight: 600;">Cliente Mayorista</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="footer">
    Clasificador Retail Inteligente | Modelo RandomForest entrenado con datos sinteticos de retail<br>
    <strong>Aviso:</strong> Las predicciones de este modelo deben usarse como herramienta de apoyo,
    no como unica fuente de decision comercial.
</div>
""",
    unsafe_allow_html=True,
)
