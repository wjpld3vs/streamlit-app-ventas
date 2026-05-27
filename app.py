"""
Dashboard de Clasificacion Retail - Prediccion de Clientes Mayoristas vs Minoristas
----------------------------------------------------------------------
Aplicacion Streamlit profesional con cuatro modulos:
  1. Prediccion Individual - Clasificacion con gauge, waterfall y contribucion por feature
  2. Carga por Lote (CSV) - Procesamiento batch con KPIs, analisis temporal y exportacion
  3. Analisis del Modelo - Feature importance, metricas, matriz de confusion, ROC, superficie de decision
  4. Escenarios What-If - Simulador interactivo de sensibilidad y comparador A/B

Modelo: RandomForestClassifier (scikit-learn) | 3 features numericas | 2 clases
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc, classification_report
)
from datetime import datetime

# ===========================================================================
# Configuracion de la pagina
# ===========================================================================
st.set_page_config(
    page_title="Clasificacion Retail | Prediccion Mayorista/Minorista",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===========================================================================
# CSS personalizado para diseno moderno profesional
# ===========================================================================
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    :root {
        --rojo-mayorista: #e94560;
        --rojo-mayorista-bg: #fff5f5;
        --rojo-mayorista-border: #fecaca;
        --azul-minorista: #3b82f6;
        --azul-minorista-bg: #eff6ff;
        --azul-minorista-border: #bfdbfe;
        --verde-alta: #10b981;
        --ambar-media: #f59e0b;
        --gris-baja: #ef4444;
        --fondo-oscuro: #0f172a;
        --texto-principal: #1e293b;
        --texto-secundario: #64748b;
        --borde-suave: #e2e8f0;
    }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 3rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #e94560;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1rem;
        color: #a8b2d1;
        margin: 0;
    }

    .result-card {
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .result-card:hover { transform: translateY(-2px); }
    .result-card.mayorista {
        background: linear-gradient(145deg, #fff5f5, #ffe0e0);
        border: 2px solid #e94560;
    }
    .result-card.minorista {
        background: linear-gradient(145deg, #eff6ff, #dbeafe);
        border: 2px solid #3b82f6;
    }
    .prediction-label {
        font-size: 3rem;
        font-weight: 800;
        margin: 0.3rem 0;
        letter-spacing: -1px;
    }
    .prediction-label.mayorista { color: #e94560; }
    .prediction-label.minorista { color: #3b82f6; }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }
    .kpi-card .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .kpi-card .kpi-label {
        font-size: 0.78rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
    }
    .kpi-card .kpi-delta {
        font-size: 0.75rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s;
        border: 1px solid #e2e8f0;
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
        font-size: 1.15rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e94560;
        display: inline-block;
    }

    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #9ca3af;
        font-size: 0.82rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #e94560, #c23152);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.45);
    }
    .stButton > button:active { transform: translateY(0); }

    .sidebar-info {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        font-size: 0.82rem;
        color: #6b7280;
        border-left: 3px solid #e94560;
    }

    .nav-radio [role="radiogroup"] label {
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.3rem;
        transition: all 0.2s;
    }

    .stDataFrame td {
        font-size: 0.85rem;
    }

    .confidence-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .confidence-badge.alta { background: #d1fae5; color: #065f46; }
    .confidence-badge.media { background: #fef3c7; color: #92400e; }
    .confidence-badge.baja { background: #fee2e2; color: #991b1b; }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.5rem 0;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ===========================================================================
# Carga del modelo (cacheado)
# ===========================================================================

@st.cache_resource
def cargar_modelo(ruta_modelo: str):
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(
            f"No se encontro el archivo del modelo en: {ruta_modelo}\n"
            "Asegurese de colocar 'modelo_clasificacion_retail.pkl' en la raiz del proyecto."
        )
    return joblib.load(ruta_modelo)


# ===========================================================================
# Constantes del modelo
# ===========================================================================
RUTA_MODELO = "modelo_clasificacion_retail.pkl"
COLUMNAS_MODELO = ["cantidad_kg", "precio_unitario", "descuento_pct"]
MAPA_CLASES = {0: "Minorista", 1: "Mayorista"}
COLOR_CLASES = {0: "#3b82f6", 1: "#e94560"}
COLOR_CLASES_BG = {0: "#eff6ff", 1: "#fff5f5"}

# Archivos CSV de prueba disponibles
CSVS_PRUEBA = {
    "datos_prueba_50.csv": "50 transacciones (ene-feb 2026)",
    "datos_prueba_200.csv": "200 transacciones (ene-abr 2026)",
    "datos_prueba_500.csv": "500 transacciones (ene-jun 2026)",
}

# ===========================================================================
# Carga del modelo con manejo de errores
# ===========================================================================
try:
    modelo = cargar_modelo(RUTA_MODELO)
    modelo_cargado = True
    FEATURE_IMPORTANCES = modelo.feature_importances_
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    modelo_cargado = False
    FEATURE_IMPORTANCES = np.array([0.33, 0.33, 0.34])
except Exception as e:
    st.error(f"Error inesperado al cargar el modelo: {e}")
    modelo_cargado = False
    FEATURE_IMPORTANCES = np.array([0.33, 0.33, 0.34])

# ===========================================================================
# Funciones auxiliares
# ===========================================================================

def construir_dataframe(cantidad_kg, precio_unitario, descuento_pct):
    return pd.DataFrame(
        [[cantidad_kg, precio_unitario, descuento_pct]],
        columns=COLUMNAS_MODELO,
    )


def obtener_interpretacion(clase_predicha, probabilidad):
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


def obtener_tier_confianza(prob):
    if prob >= 0.9:
        return "Alta"
    elif prob >= 0.7:
        return "Media"
    else:
        return "Baja"


def validar_csv(df, requeridas):
    faltantes = [c for c in requeridas if c not in df.columns]
    if faltantes:
        return False, f"Faltan columnas requeridas: {', '.join(faltantes)}"
    for c in requeridas:
        if not pd.api.types.is_numeric_dtype(df[c]):
            return False, f"La columna '{c}' debe ser numerica."
    return True, ""


def cargar_csv_prueba(nombre_archivo):
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    return None


# ===========================================================================
# Generadores de graficos Plotly
# ===========================================================================

def crear_gauge_confianza(probabilidad, titulo="Confianza del Modelo"):
    color = "#10b981" if probabilidad >= 0.9 else ("#f59e0b" if probabilidad >= 0.7 else "#ef4444")
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probabilidad * 100,
        number={"suffix": "%", "font": {"size": 36, "color": "#1e293b"}},
        delta={"reference": 70, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}},
        title={"text": titulo, "font": {"size": 14, "color": "#64748b"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": color, "thickness": 0.2},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": "#e2e8f0",
            "steps": [
                {"range": [0, 70], "color": "#fee2e2"},
                {"range": [70, 90], "color": "#fef3c7"},
                {"range": [90, 100], "color": "#d1fae5"},
            ],
            "threshold": {
                "line": {"color": "#1e293b", "width": 3},
                "thickness": 0.8,
                "value": probabilidad * 100,
            },
        },
    ))
    fig.update_layout(height=250, margin=dict(t=30, b=10, l=20, r=20))
    return fig


def crear_barras_probabilidades(prob_may, prob_min):
    fig = go.Figure(data=[
        go.Bar(
            x=[prob_may * 100, prob_min * 100],
            y=["Mayorista", "Minorista"],
            orientation="h",
            marker_color=["#e94560", "#3b82f6"],
            text=[f"{prob_may:.1%}", f"{prob_min:.1%}"],
            textposition="auto",
            textfont={"color": "white", "size": 16, "family": "Inter"},
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Probabilidad (%)", range=[0, 100], ticksuffix="%", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title=""),
        margin=dict(t=10, b=10, l=10, r=10),
        height=180,
        plot_bgcolor="white",
        bargap=0.4,
    )
    return fig


def crear_feature_importance_plot(importances, feature_names, n_features=None):
    if n_features is None:
        n_features = len(feature_names)
    idx = np.argsort(importances)[-n_features:]
    fig = go.Figure(data=[
        go.Bar(
            x=importances[idx] * 100,
            y=[feature_names[i] for i in idx],
            orientation="h",
            marker=dict(
                color=importances[idx] * 100,
                colorscale=[[0, "#bfdbfe"], [0.5, "#3b82f6"], [1, "#e94560"]],
                showscale=False,
            ),
            text=[f"{v:.1f}%" for v in importances[idx] * 100],
            textposition="outside",
            textfont={"color": "#1e293b", "size": 13},
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Importancia (%)", showgrid=True, gridcolor="#f1f5f9", ticksuffix="%"),
        yaxis=dict(title=""),
        margin=dict(t=10, b=10, l=10, r=30),
        height=200 + 30 * n_features,
        plot_bgcolor="white",
    )
    return fig


def crear_feature_contribucion_waterfall(input_values, importances, feature_names, clase_predicha):
    """
    Muestra barras horizontales con la magnitud de cada feature y su direccion
    de influencia (hacia Mayorista o Minorista).
    """
    valores = np.array(input_values)
    colores = []
    etiquetas_direccion = []

    # Usamos la importancia como "peso" y la magnitud relativa del valor
    # para estimar contribucion. Simplificado pero informativo.
    # Para cada feature, estimamos si "empuja" hacia Mayorista o Minorista
    # basandonos en si valores altos significan Mayorista.
    # cantidades altas y descuentos altos -> Mayorista
    # precios altos con baja cantidad -> Minorista

    # Normalizamos valores para escalar
    rangos = {"cantidad_kg": (1, 500), "precio_unitario": (0.01, 500), "descuento_pct": (0, 100)}
    direcciones = {"cantidad_kg": 1, "precio_unitario": -1, "descuento_pct": 1}  # 1 = valores altos favorecen Mayorista

    contribuciones = []
    for i, name in enumerate(feature_names):
        rmin, rmax = rangos[name]
        valor_norm = (valores[i] - rmin) / (rmax - rmin) if rmax != rmin else 0.5
        contrib = importances[i] * valor_norm * direcciones[name]
        contribuciones.append(contrib)

    # Escalar contribuciones para visualizacion (valores absolutos)
    max_abs = max(abs(c) for c in contribuciones) if any(abs(c) > 0 for c in contribuciones) else 1
    contribuciones_scaled = [c / max_abs * 100 for c in contribuciones]

    for i, (c_scaled, c_raw) in enumerate(zip(contribuciones_scaled, contribuciones)):
        if c_raw > 0:
            colores.append("#e94560")
            etiquetas_direccion.append(" Mayorista")
        else:
            colores.append("#3b82f6")
            etiquetas_direccion.append(" Minorista")

    fig = go.Figure(data=[
        go.Bar(
            x=contribuciones_scaled,
            y=feature_names,
            orientation="h",
            marker_color=colores,
            text=[f"{abs(v):.0f}%" if abs(v) > 1 else "" for v in contribuciones_scaled],
            textposition="outside",
            textfont={"color": "#1e293b", "size": 12},
            hovertemplate="%{y}: contribucion %{customdata[0]:+.2f}<br>Valor: %{customdata[1]}<extra></extra>",
            customdata=list(zip(contribuciones, valores)),
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Contribucion relativa a la prediccion", showgrid=True, gridcolor="#f1f5f9", zeroline=True, zerolinecolor="#cbd5e1"),
        yaxis=dict(title=""),
        margin=dict(t=10, b=10, l=10, r=30),
        height=200,
        plot_bgcolor="white",
        shapes=[
            dict(type="line", x0=0, x1=0, y0=-0.5, y1=len(feature_names) - 0.5,
                 line=dict(color="#94a3b8", width=1, dash="dash"), layer="below"),
        ],
    )
    return fig


def crear_donut_clases(n_may, n_min):
    fig = go.Figure(data=[
        go.Pie(
            labels=["Mayorista", "Minorista"],
            values=[n_may, n_min],
            hole=0.55,
            marker_colors=["#e94560", "#3b82f6"],
            textinfo="label+percent",
            textfont={"size": 13, "color": "#1e293b", "family": "Inter"},
            hovertemplate="%{label}: %{value} transacciones (%{percent})<extra></extra>",
        )
    ])
    fig.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        height=320,
        annotations=[dict(text=f"Total<br>{n_may + n_min}", x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#1e293b")],
    )
    return fig


def crear_histograma_probabilidades(probs_may):
    fig = px.histogram(
        x=probs_may * 100,
        nbins=25,
        labels={"x": "Probabilidad de Mayorista (%)", "y": "Frecuencia"},
        color_discrete_sequence=["#6366f1"],
        opacity=0.75,
    )
    fig.update_layout(
        xaxis=dict(title="Probabilidad de Mayorista (%)", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Num. Transacciones", showgrid=True, gridcolor="#f1f5f9"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        plot_bgcolor="white",
        bargap=0.05,
    )
    fig.add_vline(x=50, line_dash="dash", line_color="#94a3b8", annotation_text="Frontera", annotation_position="top right")
    return fig


def crear_serie_temporal(df_resultados, frecuencia="D"):
    if "fecha" not in df_resultados.columns:
        return None
    df = df_resultados.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    if frecuencia == "D":
        freq_label = "Diario"
        grouper = pd.Grouper(key="fecha", freq="D")
    elif frecuencia == "W":
        freq_label = "Semanal"
        grouper = pd.Grouper(key="fecha", freq="W")
    else:
        freq_label = "Mensual"
        grouper = pd.Grouper(key="fecha", freq="M")

    agrupado = df.groupby(grouper).agg(
        total=("clase_predicha", "count"),
        mayoristas=("clase_predicha", "sum"),
        confianza_media=("prob_mayorista_confianza", "mean"),
        importe_total=("importe_total", "sum"),
    ).reset_index()
    agrupado = agrupado[agrupado["total"] > 0].copy()
    agrupado["pct_mayoristas"] = agrupado["mayoristas"] / agrupado["total"] * 100

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=agrupado["fecha"], y=agrupado["pct_mayoristas"],
            name="% Mayorista", mode="lines+markers",
            line=dict(color="#e94560", width=2.5), marker=dict(size=6),
            fill="tozeroy", fillcolor="rgba(233,69,96,0.1)",
            hovertemplate="%{y:.1f}%<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=agrupado["fecha"], y=agrupado["total"],
            name="Transacciones", mode="lines+markers",
            line=dict(color="#6366f1", width=2, dash="dot"), marker=dict(size=5),
            hovertemplate="%{y}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="% Mayorista", secondary_y=False, ticksuffix="%")
    fig.update_yaxes(title_text="Num. Transacciones", secondary_y=True)
    fig.update_layout(
        title=f"Evolucion Temporal - {freq_label}",
        hovermode="x unified",
        margin=dict(t=40, b=10, l=10, r=10),
        height=350,
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def crear_barras_confianza(df_resultados):
    """Barras apiladas: conteo por tier de confianza, segmentado por clase."""
    df = df_resultados.copy()
    df["tier"] = df["prob_mayorista_confianza"].apply(lambda p: obtener_tier_confianza(p))
    df["clase_nombre"] = df["clase_predicha"].map({1: "Mayorista", 0: "Minorista"})

    cruzado = pd.crosstab(df["tier"], df["clase_nombre"])
    for c in ["Minorista", "Mayorista"]:
        if c not in cruzado.columns:
            cruzado[c] = 0
    orden_tiers = ["Alta", "Media", "Baja"]
    cruzado = cruzado.reindex([t for t in orden_tiers if t in cruzado.index], fill_value=0)

    fig = go.Figure(data=[
        go.Bar(
            name="Mayorista", y=cruzado.index, x=cruzado["Mayorista"],
            orientation="h", marker_color="#e94560", text=cruzado["Mayorista"].tolist(),
            textposition="inside", textfont={"color": "white"},
        ),
        go.Bar(
            name="Minorista", y=cruzado.index, x=cruzado["Minorista"],
            orientation="h", marker_color="#3b82f6", text=cruzado["Minorista"].tolist(),
            textposition="inside", textfont={"color": "white"},
        ),
    ])
    fig.update_layout(
        barmode="stack",
        xaxis=dict(title="Num. Transacciones", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Nivel de Confianza"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=220,
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def crear_superficie_decision(modelo_local, feature_names):
    """Crea un scatter plot mostrando la superficie de decision para cantidad_kg vs precio_unitario."""
    # Fijamos descuento_pct en un valor medio
    descuento_fijo = 15
    n_grid = 50

    kg_range = np.linspace(1, 500, n_grid)
    precio_range = np.linspace(0.5, 200, n_grid)  # Reducimos rango para mejor visualizacion
    kg_grid, precio_grid = np.meshgrid(kg_range, precio_range)

    X_grid = np.column_stack([kg_grid.ravel(), precio_grid.ravel(), np.full(n_grid * n_grid, descuento_fijo)])
    Z = modelo_local.predict_proba(X_grid)[:, 1].reshape(n_grid, n_grid)

    fig = go.Figure(data=[
        go.Heatmap(
            x=kg_range, y=precio_range, z=Z,
            colorscale=[[0, "#3b82f6"], [0.5, "#a78bfa"], [1, "#e94560"]],
            zmin=0, zmax=1,
            colorbar=dict(title="P(Mayorista)", titleside="right", tickformat=".0%"),
            hovertemplate="Cantidad: %{x} kg<br>Precio: $%{y:.2f}<br>P(Mayorista): %{z:.1%}<extra></extra>",
            name="",
            showscale=True,
        )
    ])
    fig.update_layout(
        xaxis=dict(title="Cantidad (kg)"),
        yaxis=dict(title="Precio Unitario ($)"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=400,
        plot_bgcolor="white",
        title=f"Superficie de Decision (descuento = {descuento_fijo}%)",
    )
    return fig


def crear_matriz_confusion_plot(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    etiquetas = ["Minorista", "Mayorista"]

    fig = px.imshow(
        cm,
        x=etiquetas, y=etiquetas,
        text_auto=True,
        color_continuous_scale=[[0, "#f1f5f9"], [0.5, "#bfdbfe"], [1, "#3b82f6"]],
    )
    fig.update_layout(
        xaxis=dict(title="Predicho", side="bottom"),
        yaxis=dict(title="Real"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=320,
    )
    fig.update_traces(textfont={"size": 22, "color": "#1e293b"})
    return fig


def crear_curva_roc_plot(y_true, y_proba):
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)

    fig = go.Figure(data=[
        go.Scatter(
            x=fpr, y=tpr,
            mode="lines",
            name=f"ROC (AUC = {roc_auc:.3f})",
            line=dict(color="#e94560", width=3),
            fill="tozeroy",
            fillcolor="rgba(233,69,96,0.1)",
            hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>",
        ),
        go.Scatter(
            x=[0, 1], y=[0, 1],
            mode="lines",
            name="Aleatorio (AUC = 0.5)",
            line=dict(color="#94a3b8", width=1.5, dash="dash"),
            hoverinfo="skip",
        ),
    ])
    fig.update_layout(
        xaxis=dict(title="Tasa de Falsos Positivos (FPR)", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Tasa de Verdaderos Positivos (TPR)", showgrid=True, gridcolor="#f1f5f9"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def crear_curva_sensibilidad_plot(modelo_local, feature_names, feature_var, rango, valores_fijos):
    """Curva de sensibilidad: como cambia la probabilidad al variar una feature."""
    X_base = []
    for fn in feature_names:
        if fn == feature_var:
            X_base.append(rango)
        else:
            X_base.append(np.full(len(rango), valores_fijos.get(fn, 0)))
    X_mat = np.column_stack(X_base)
    probs = modelo_local.predict_proba(X_mat)[:, 1]

    fig = go.Figure(data=[
        go.Scatter(
            x=rango, y=probs * 100,
            mode="lines+markers",
            line=dict(color="#e94560", width=3),
            marker=dict(size=6, color=probs * 100, colorscale=[[0, "#3b82f6"], [0.5, "#a78bfa"], [1, "#e94560"]], showscale=False),
            fill="tozeroy",
            fillcolor="rgba(233,69,96,0.1)",
            hovertemplate=f"{feature_var}: %{{x}}<br>P(Mayorista): %{{y:.1f}}%<extra></extra>",
        )
    ])
    fig.add_hline(y=50, line_dash="dash", line_color="#94a3b8", annotation_text="Umbral 50%", annotation_position="right")
    fig.update_layout(
        xaxis=dict(title=feature_var, showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Probabilidad Mayorista (%)", ticksuffix="%", range=[0, 105], showgrid=True, gridcolor="#f1f5f9"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=320,
        plot_bgcolor="white",
    )
    return fig


# ===========================================================================
# Cabecera principal
# ===========================================================================
st.markdown(
    """
<div class="main-header">
    <h1>Clasificador Retail Inteligente</h1>
    <p>Prediccion de perfil de cliente: Mayorista vs Minorista &mdash; Modo individual, lote, analisis y escenarios</p>
</div>
""",
    unsafe_allow_html=True,
)

# ===========================================================================
# Sidebar - Navegacion principal
# ===========================================================================
st.sidebar.markdown(
    """
<div style="text-align: center; padding-bottom: 0.5rem;">
    <h2 style="color: #e94560; margin: 0; font-size: 1.3rem;">Navegacion</h2>
</div>
""",
    unsafe_allow_html=True,
)

pagina = st.sidebar.radio(
    "Seleccione modulo",
    ["Prediccion Individual", "Carga por Lote (CSV)", "Analisis del Modelo", "Escenarios What-If"],
    key="pagina_activa",
    label_visibility="collapsed",
)

st.sidebar.markdown("---")

# Info del modelo (siempre visible)
if modelo_cargado:
    st.sidebar.markdown(
        f"""
<div class="sidebar-info">
    <strong>RandomForestClassifier</strong><br>
    <strong>Features:</strong> {', '.join(COLUMNAS_MODELO)}<br>
    <strong>Clases:</strong> Minorista (0), Mayorista (1)<br>
    <strong>Probabilidades:</strong> Disponible
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.sidebar.error("Modelo no cargado")

# ===========================================================================
# Inicializacion de session state global
# ===========================================================================
if "prediccion_individual" not in st.session_state:
    st.session_state.prediccion_individual = False
if "resultados_batch" not in st.session_state:
    st.session_state.resultados_batch = None
if "df_batch_original" not in st.session_state:
    st.session_state.df_batch_original = None
if "datos_comparador_a" not in st.session_state:
    st.session_state.datos_comparador_a = None
if "datos_comparador_b" not in st.session_state:
    st.session_state.datos_comparador_b = None

# ===========================================================================
# ===========================================================================
# MODULO 1: PREDICCION INDIVIDUAL
# ===========================================================================
# ===========================================================================
if pagina == "Prediccion Individual":
    st.sidebar.markdown(
        """
<div style="text-align: center; padding-bottom: 0.5rem;">
    <h3 style="color: #1e293b; margin: 0;">Parametros de Entrada</h3>
    <p style="color: #6b7280; font-size: 0.78rem;">Ajuste los valores y presione <b>Clasificar</b></p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    cantidad_kg = st.sidebar.number_input(
        "Cantidad (kg)", min_value=1, max_value=500, value=100, step=1,
        help="Cantidad de producto en kilogramos. Rango: 1 - 500 kg.",
    )
    precio_unitario = st.sidebar.number_input(
        "Precio Unitario ($)", min_value=0.01, max_value=500.0, value=10.0, step=0.5,
        format="%.2f", help="Precio por unidad.",
    )
    descuento_pct = st.sidebar.slider(
        "Descuento (%)", min_value=0, max_value=100, value=10, step=1,
        help="Porcentaje de descuento aplicado.",
    )

    col_b1, col_b2 = st.sidebar.columns([2, 1])
    with col_b1:
        boton_clasificar = st.button("Clasificar Operacion", type="primary", use_container_width=True)

    with col_b2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.prediccion_individual = False
            st.rerun()

    st.sidebar.markdown("---")

    # --- Area principal ---
    if boton_clasificar:
        if not modelo_cargado:
            st.error("No se puede realizar la prediccion. El modelo no se cargo correctamente.")
        else:
            try:
                df_entrada = construir_dataframe(cantidad_kg, precio_unitario, descuento_pct)
                clase_predicha = modelo.predict(df_entrada)[0]
                probabilidades = modelo.predict_proba(df_entrada)[0]

                st.session_state.prediccion_individual = True
                st.session_state.clase_predicha = int(clase_predicha)
                st.session_state.probabilidades = probabilidades
                st.session_state.etiqueta_clase = MAPA_CLASES.get(int(clase_predicha), f"Clase {clase_predicha}")
                st.session_state.prob_mayorista = probabilidades[1]
                st.session_state.prob_minorista = probabilidades[0]
                st.session_state.df_entrada = df_entrada
                st.session_state.cantidad_kg = cantidad_kg
                st.session_state.precio_unitario = precio_unitario
                st.session_state.descuento_pct = descuento_pct
                st.rerun()

            except Exception as e:
                st.error(f"Error al generar la prediccion: {e}")

    if st.session_state.prediccion_individual:
        st.markdown('<p class="section-title">Resultado de la Clasificacion</p>', unsafe_allow_html=True)

        clase = st.session_state.clase_predicha
        prob_may = st.session_state.prob_mayorista
        prob_min = st.session_state.prob_minorista
        etiqueta = st.session_state.etiqueta_clase
        kg = st.session_state.cantidad_kg
        precio = st.session_state.precio_unitario
        desc = st.session_state.descuento_pct

        # --- Fila 1: Tarjeta de resultado + Gauge ---
        col_card, col_gauge = st.columns([1, 1])

        with col_card:
            css_clase = "mayorista" if clase == 1 else "minorista"
            texto_etiqueta = "MAYORISTA" if clase == 1 else "MINORISTA"
            st.markdown(
                f"""
            <div class="result-card {css_clase}">
                <div style="font-size: 0.85rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px;">
                    Clasificacion
                </div>
                <div class="prediction-label {css_clase}">{texto_etiqueta}</div>
                <div style="font-size: 0.95rem; color: #6b7280;">
                    Confianza: <strong>{prob_may if clase == 1 else prob_min:.1%}</strong>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_gauge:
            prob_confianza = prob_may if clase == 1 else prob_min
            fig_gauge = crear_gauge_confianza(prob_confianza)
            st.plotly_chart(fig_gauge, use_container_width=True, key="gauge_individual")

        # --- Fila 2: Metricas en columnas ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="metric-box"><div class="value">{prob_may:.1%}</div><div class="label">Probabilidad Mayorista</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-box"><div class="value">{prob_min:.1%}</div><div class="label">Probabilidad Minorista</div></div>""", unsafe_allow_html=True)
        with col3:
            importe_total = kg * precio * (1 - desc / 100)
            st.markdown(f"""<div class="metric-box"><div class="value">${importe_total:,.2f}</div><div class="label">Importe Total Estimado</div></div>""", unsafe_allow_html=True)

        # --- Fila 3: Grafico de probabilidades + Interpretacion ---
        st.markdown('<p class="section-title">Analisis de la Prediccion</p>', unsafe_allow_html=True)
        col_chart, col_interp = st.columns([1, 1])

        with col_chart:
            fig_barras = crear_barras_probabilidades(prob_may, prob_min)
            st.plotly_chart(fig_barras, use_container_width=True, key="barras_prob_individual")

        with col_interp:
            st.markdown("#### Interpretacion del modelo")
            mensaje = obtener_interpretacion(clase, prob_may if clase == 1 else prob_min)
            if clase == 1:
                st.success(mensaje)
            else:
                st.info(mensaje)

        # --- Fila 4: Waterfall de contribucion por feature ---
        st.markdown('<p class="section-title">Contribucion de cada Variable a la Prediccion</p>', unsafe_allow_html=True)
        valores_input = [kg, precio, desc]
        fig_waterfall = crear_feature_contribucion_waterfall(
            valores_input, FEATURE_IMPORTANCES, COLUMNAS_MODELO, clase
        )
        st.plotly_chart(fig_waterfall, use_container_width=True, key="waterfall_individual")
        st.caption("Las barras rojas indican que el valor de la variable favorece la clasificacion como Mayorista. Las azules favorecen Minorista. La longitud refleja la importancia relativa de cada feature ponderada por el valor ingresado.")

        # --- Fila 5: Datos de entrada + Recomendacion accionable ---
        with st.expander("Ver datos de entrada y recomendaciones"):
            col_debug, col_recom = st.columns([1, 1])
            with col_debug:
                st.dataframe(st.session_state.df_entrada, use_container_width=True)
                st.caption("Valores exactos enviados al modelo.")
            with col_recom:
                tier = obtener_tier_confianza(prob_may if clase == 1 else prob_min)
                st.markdown("#### Acciones recomendadas")
                recomendaciones = {
                    ("Mayorista", "Alta"): [
                        "Aplicar tarifa mayorista sin restricciones",
                        "Asignar ejecutivo de cuenta dedicado",
                        "Incluir en programa de fidelizacion B2B",
                    ],
                    ("Mayorista", "Media"): [
                        "Aplicar tarifa mayorista con verificacion",
                        "Revisar historial antes de aprobar credito",
                        "Ofrecer condiciones especiales condicionadas",
                    ],
                    ("Mayorista", "Baja"): [
                        "Analisis manual requerido antes de decidir",
                        "Verificar referencias comerciales del cliente",
                        "Considerar periodo de prueba con tarifa intermedia",
                    ],
                    ("Minorista", "Alta"): [
                        "Aplicar precios de venta al publico",
                        "No requiere aprobacion adicional",
                        "Enviar a proceso de venta estandar",
                    ],
                    ("Minorista", "Media"): [
                        "Aplicar precios standard",
                        "Monitorear si el cliente incrementa volumen",
                        "Mantener en base de datos para seguimiento",
                    ],
                    ("Minorista", "Baja"): [
                        "Revisar si cliente puede ser mayorista ocasional",
                        "Considerar descuento por volumen futuro",
                        "Documentar caso para revision periodica",
                    ],
                }
                for rec in recomendaciones.get((etiqueta, tier), ["Analisis manual complementario requerido"]):
                    st.markdown(f"- {rec}")

    else:
        st.markdown(
            """
        <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
            <div style="font-size: 4rem; margin-bottom: 1rem;"></div>
            <h3 style="color: #374151; margin-bottom: 0.5rem;">Ajuste los parametros y presione <b>Clasificar Operacion</b></h3>
            <p style="font-size: 0.95rem;">
                Use la barra lateral para configurar los valores de la operacion.
                El modelo clasificara automaticamente el perfil del cliente.
            </p>
            <div style="margin-top: 2rem; padding: 1rem; background: #f9fafb; border-radius: 8px; display: inline-block; text-align: left;">
                <strong>Sugerencia rapida:</strong><br>
                Pruebe: cantidad = <b>400 kg</b>, precio = <b>$10</b>, descuento = <b>15%</b><br>
                Resultado esperado: <span style="color: #e94560; font-weight: 600;">Cliente Mayorista</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# ===========================================================================
# MODULO 2: CARGA POR LOTE (CSV)
# ===========================================================================
# ===========================================================================
elif pagina == "Carga por Lote (CSV)":
    st.sidebar.markdown(
        """
<div style="text-align: center; padding-bottom: 0.5rem;">
    <h3 style="color: #1e293b; margin: 0;">Carga de Datos</h3>
    <p style="color: #6b7280; font-size: 0.78rem;">Suba un CSV o use datos de prueba</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Opcion: usar CSV de prueba
    csv_seleccionado = st.sidebar.selectbox(
        "Datos de prueba pre-cargados",
        ["Ninguno (subir archivo propio)"] + [f"{k} ({v})" for k, v in CSVS_PRUEBA.items()],
        help="Seleccione un dataset de prueba generado automaticamente.",
    )

    archivo_subido = None
    if csv_seleccionado.startswith("Ninguno"):
        archivo_subido = st.sidebar.file_uploader(
            "Subir archivo CSV",
            type=["csv"],
            help="El CSV debe contener al menos las columnas: cantidad_kg, precio_unitario, descuento_pct. Opcional: fecha, clase_real.",
        )
    else:
        nombre_csv = csv_seleccionado.split(" (")[0]
        if os.path.exists(nombre_csv):
            archivo_subido = nombre_csv
            st.sidebar.success(f"Dataset cargado: {nombre_csv}")
            st.sidebar.caption(f"Archivo local: {len(pd.read_csv(nombre_csv))} filas listas para procesar.")
        else:
            st.sidebar.error(f"Archivo no encontrado: {nombre_csv}")
            archivo_subido = None

    st.sidebar.markdown("---")

    # Filtros para la visualizacion (se muestran despues de procesar)
    st.sidebar.markdown("#### Filtros de visualizacion")
    filtro_clase = st.sidebar.selectbox("Filtrar por clase", ["Todas", "Mayorista", "Minorista"], key="filtro_clase_batch")
    filtro_confianza = st.sidebar.selectbox("Filtrar por confianza", ["Todos", "Alta", "Media", "Baja"], key="filtro_confianza_batch")
    umbral_confianza = st.sidebar.slider("Umbral de decision", 0.0, 1.0, 0.5, 0.05, key="umbral_batch",
                                         help="Ajuste el umbral para reclasificar. Default: 0.5")

    # --- Area principal ---
    if archivo_subido is not None:
        try:
            if isinstance(archivo_subido, str):
                df_original = pd.read_csv(archivo_subido)
                origen = "dataset de prueba"
            else:
                df_original = pd.read_csv(archivo_subido)
                origen = "archivo subido"

            valido, msg = validar_csv(df_original, COLUMNAS_MODELO)
            if not valido:
                st.error(f"Error de validacion: {msg}")
            else:
                st.session_state.df_batch_original = df_original

                # Prediccion batch
                with st.spinner("Procesando transacciones..."):
                    X_batch = df_original[COLUMNAS_MODELO].copy()
                    predicciones = modelo.predict(X_batch)
                    probabilidades = modelo.predict_proba(X_batch)

                    df_resultados = df_original.copy()
                    df_resultados["clase_predicha"] = predicciones
                    df_resultados["prob_mayorista"] = probabilidades[:, 1]
                    df_resultados["prob_minorista"] = probabilidades[:, 0]
                    df_resultados["prob_mayorista_confianza"] = probabilidades[:, 1]
                    df_resultados["importe_total"] = (
                        df_resultados["cantidad_kg"] * df_resultados["precio_unitario"] * (1 - df_resultados["descuento_pct"] / 100)
                    )
                    df_resultados["tier_confianza"] = df_resultados["prob_mayorista_confianza"].apply(obtener_tier_confianza)
                    df_resultados["clase_nombre"] = df_resultados["clase_predicha"].map(MAPA_CLASES)

                    # Reclasificar segun umbral
                    if umbral_confianza != 0.5:
                        df_resultados["clase_predicha"] = (df_resultados["prob_mayorista"] >= umbral_confianza).astype(int)
                        df_resultados["clase_nombre"] = df_resultados["clase_predicha"].map(MAPA_CLASES)
                        df_resultados["prob_mayorista_confianza"] = df_resultados.apply(
                            lambda r: r["prob_mayorista"] if r["clase_predicha"] == 1 else r["prob_minorista"], axis=1
                        )
                        df_resultados["tier_confianza"] = df_resultados["prob_mayorista_confianza"].apply(obtener_tier_confianza)

                    st.session_state.resultados_batch = df_resultados

                st.success(f"Se procesaron {len(df_resultados)} transacciones desde {origen}.")

                # --- KPIs de resumen ---
                total = len(df_resultados)
                n_may = (df_resultados["clase_predicha"] == 1).sum()
                n_min = (df_resultados["clase_predicha"] == 0).sum()
                confianza_media = df_resultados["prob_mayorista_confianza"].mean()
                importe_total_batch = df_resultados["importe_total"].sum()
                n_zona_gris = (df_resultados["tier_confianza"] == "Baja").sum()

                st.markdown('<p class="section-title">Resumen del Lote</p>', unsafe_allow_html=True)
                cols_kpi = st.columns(6)
                kpis = [
                    (str(total), "Transacciones", "#6366f1", ""),
                    (f"{n_may/total*100:.1f}%" if total > 0 else "0%", "% Mayorista", "#e94560", f"{n_may} ops"),
                    (f"{n_min/total*100:.1f}%" if total > 0 else "0%", "% Minorista", "#3b82f6", f"{n_min} ops"),
                    (f"{confianza_media:.1%}", "Confianza Media", "#10b981", ""),
                    (f"${importe_total_batch:,.0f}", "Importe Total", "#f59e0b", ""),
                    (str(n_zona_gris), "Zona Gris", "#ef4444", "Baja confianza"),
                ]
                for i, (valor, label, color, delta) in enumerate(kpis):
                    with cols_kpi[i]:
                        st.markdown(
                            f"""
                        <div class="kpi-card">
                            <div class="kpi-value" style="color: {color};">{valor}</div>
                            <div class="kpi-label">{label}</div>
                            <div class="kpi-delta" style="color: {color};">{delta}</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                st.markdown("---")

                # --- Graficos del lote ---
                col_graf1, col_graf2 = st.columns([1, 1])

                with col_graf1:
                    st.markdown("#### Distribucion de Clases")
                    fig_donut = crear_donut_clases(n_may, n_min)
                    st.plotly_chart(fig_donut, use_container_width=True, key="donut_batch")

                with col_graf2:
                    st.markdown("#### Distribucion de Probabilidades")
                    fig_hist = crear_histograma_probabilidades(df_resultados["prob_mayorista"])
                    st.plotly_chart(fig_hist, use_container_width=True, key="hist_batch")

                col_graf3, col_graf4 = st.columns([1, 1])

                with col_graf3:
                    st.markdown("#### Confianza por Clase")
                    fig_confianza = crear_barras_confianza(df_resultados)
                    st.plotly_chart(fig_confianza, use_container_width=True, key="confianza_batch")

                with col_graf4:
                    st.markdown("#### Evolucion Temporal")
                    if "fecha" in df_resultados.columns:
                        freq_sel = st.selectbox("Frecuencia", ["Diario", "Semanal", "Mensual"], key="freq_batch",
                                                help="Agrupacion temporal para el grafico.")
                        freq_map = {"Diario": "D", "Semanal": "W", "Mensual": "M"}
                        fig_ts = crear_serie_temporal(df_resultados, freq_map[freq_sel])
                        if fig_ts:
                            st.plotly_chart(fig_ts, use_container_width=True, key="ts_batch")
                    else:
                        st.info("El dataset no tiene columna 'fecha'. Agreguela para ver evolucion temporal.")

                st.markdown("---")

                # --- Tabla de resultados con filtros ---
                st.markdown('<p class="section-title">Resultados Detallados</p>', unsafe_allow_html=True)

                df_mostrar = df_resultados.copy()
                if filtro_clase != "Todas":
                    df_mostrar = df_mostrar[df_mostrar["clase_nombre"] == filtro_clase]
                if filtro_confianza != "Todos":
                    df_mostrar = df_mostrar[df_mostrar["tier_confianza"] == filtro_confianza]

                st.caption(f"Mostrando {len(df_mostrar)} de {len(df_resultados)} transacciones")

                columnas_mostrar = [c for c in ["fecha", "cantidad_kg", "precio_unitario", "descuento_pct",
                                                  "clase_nombre", "prob_mayorista", "prob_minorista",
                                                  "tier_confianza", "importe_total", "clase_real"]
                                    if c in df_mostrar.columns]

                # Aplicar estilo condicional
                def color_filas(row):
                    if row.get("clase_nombre") == "Mayorista":
                        return ["background-color: #fff5f5" if col == "clase_nombre" else "background-color: #fef2f2" for col in row.index]
                    else:
                        return ["background-color: #eff6ff" if col == "clase_nombre" else "background-color: #f8faff" for col in row.index]

                st.dataframe(
                    df_mostrar[columnas_mostrar].style
                    .format({"prob_mayorista": "{:.1%}", "prob_minorista": "{:.1%}", "importe_total": "${:,.2f}"})
                    .apply(color_filas, axis=1),
                    use_container_width=True, height=400,
                )

                # --- Exportacion ---
                st.markdown("---")
                col_exp1, col_exp2, col_exp3 = st.columns([2, 1, 1])
                with col_exp1:
                    csv_export = df_resultados.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Descargar resultados completos (CSV)",
                        data=csv_export,
                        file_name=f"predicciones_retail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                with col_exp2:
                    n_may_alta = len(df_resultados[(df_resultados["clase_predicha"] == 1) & (df_resultados["tier_confianza"] == "Alta")])
                    n_min_alta = len(df_resultados[(df_resultados["clase_predicha"] == 0) & (df_resultados["tier_confianza"] == "Alta")])
                    st.metric("Mayoristas alta confianza", n_may_alta)
                with col_exp3:
                    st.metric("Minoristas alta confianza", n_min_alta)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        st.markdown(
            """
        <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
            <div style="font-size: 4rem; margin-bottom: 1rem;"></div>
            <h3 style="color: #374151; margin-bottom: 0.5rem;">Carga de Datos por Lote</h3>
            <p style="font-size: 0.95rem;">
                Suba un archivo CSV con transacciones o seleccione un dataset de prueba.<br>
                El modelo procesara todas las filas y generara un analisis completo.
            </p>
            <div style="margin-top: 1.5rem; padding: 1rem; background: #f9fafb; border-radius: 8px; display: inline-block; text-align: left;">
                <strong>Formato esperado del CSV:</strong><br>
                Columnas requeridas: <code>cantidad_kg</code>, <code>precio_unitario</code>, <code>descuento_pct</code><br>
                Columnas opcionales: <code>fecha</code>, <code>clase_real</code> (para evaluacion)<br>
                <br>
                <strong>Tambien puede usar los datasets de prueba</strong> desde la barra lateral.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ===========================================================================
# ===========================================================================
# MODULO 3: ANALISIS DEL MODELO
# ===========================================================================
# ===========================================================================
elif pagina == "Analisis del Modelo":
    st.sidebar.markdown(
        """
<div style="text-align: center; padding-bottom: 0.5rem;">
    <h3 style="color: #1e293b; margin: 0;">Analisis del Modelo</h3>
    <p style="color: #6b7280; font-size: 0.78rem;">Transparencia y metricas</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Fuente de datos para evaluacion
    st.sidebar.markdown("#### Datos para evaluacion")
    csv_eval = st.sidebar.selectbox(
        "Dataset para metricas",
        ["Ninguno"] + [f"{k} ({v})" for k, v in CSVS_PRUEBA.items()],
        help="Seleccione un dataset con columna 'clase_real' para calcular metricas de rendimiento.",
        key="csv_eval_modelo",
    )

    st.sidebar.markdown("---")
    umbral_modelo = st.sidebar.slider(
        "Umbral de clasificacion",
        0.0, 1.0, 0.5, 0.05,
        help="Ajuste el umbral para ver como cambian las metricas y la superficie de decision.",
        key="umbral_modelo_analysis",
    )

    # --- Area principal ---
    st.markdown('<p class="section-title">Importancia de Features</p>', unsafe_allow_html=True)

    col_fi, col_fi_info = st.columns([2, 1])
    with col_fi:
        fig_fi = crear_feature_importance_plot(FEATURE_IMPORTANCES, COLUMNAS_MODELO)
        st.plotly_chart(fig_fi, use_container_width=True, key="fi_modelo")
    with col_fi_info:
        st.markdown("#### Que significa esto?")
        st.markdown("""
        Las **importancias de features** indican que tanto contribuye cada variable
        a la decision del modelo Random Forest.

        - **cantidad_kg**: El volumen de compra es el factor mas determinante
        - **descuento_pct**: Los descuentos altos son tipicos de mayoristas
        - **precio_unitario**: El precio ayuda a refinar la clasificacion

        Valores mas altos = mayor peso en la decision final del modelo.
        """)

    st.markdown("---")

    # Superficie de decision
    st.markdown('<p class="section-title">Superficie de Decision</p>', unsafe_allow_html=True)
    st.caption("Mapa de calor que muestra como clasifica el modelo en el espacio cantidad_kg vs precio_unitario (con descuento fijo al 15%).")

    descuento_fijo_sup = st.slider("Descuento fijo para la visualizacion", 0, 100, 15, 5, key="desc_superficie")
    
    # Regenerar con el descuento seleccionado
    n_grid = 50
    kg_range = np.linspace(1, 500, n_grid)
    precio_range = np.linspace(0.5, 200, n_grid)
    kg_grid, precio_grid = np.meshgrid(kg_range, precio_range)
    X_grid = np.column_stack([kg_grid.ravel(), precio_grid.ravel(), np.full(n_grid * n_grid, descuento_fijo_sup)])
    Z = modelo.predict_proba(X_grid)[:, 1].reshape(n_grid, n_grid)

    fig_sup = go.Figure(data=[
        go.Heatmap(
            x=kg_range, y=precio_range, z=Z,
            colorscale=[[0, "#3b82f6"], [0.5, "#a78bfa"], [1, "#e94560"]],
            zmin=0, zmax=1,
            colorbar=dict(title="P(Mayorista)", titleside="right", tickformat=".0%"),
            hovertemplate="Cantidad: %{x} kg<br>Precio: $%{y:.2f}<br>P(Mayorista): %{z:.1%}<extra></extra>",
        )
    ])
    # Linea de contorno para umbral
    fig_sup.add_trace(
        go.Contour(
            x=kg_range, y=precio_range, z=Z,
            contours=dict(start=umbral_modelo, end=umbral_modelo, size=0.01, coloring="lines"),
            line=dict(color="white", width=2),
            showscale=False,
            hoverinfo="skip",
            name=f"Umbral {umbral_modelo:.0%}",
        )
    )
    fig_sup.update_layout(
        xaxis=dict(title="Cantidad (kg)"),
        yaxis=dict(title="Precio Unitario ($)"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=420,
        plot_bgcolor="white",
        title=f"Superficie de Decision (descuento = {descuento_fijo_sup}%, umbral = {umbral_modelo:.0%})",
    )
    st.plotly_chart(fig_sup, use_container_width=True, key="superficie_modelo")

    st.markdown("---")

    # Metricas de rendimiento (si hay clase_real en el dataset seleccionado)
    if not csv_eval.startswith("Ninguno"):
        nombre_csv = csv_eval.split(" (")[0]
        if os.path.exists(nombre_csv):
            df_eval = pd.read_csv(nombre_csv)
            if "clase_real" in df_eval.columns:
                st.markdown('<p class="section-title">Metricas de Rendimiento</p>', unsafe_allow_html=True)

                X_eval = df_eval[COLUMNAS_MODELO]
                y_real = df_eval["clase_real"]
                y_proba = modelo.predict_proba(X_eval)[:, 1]
                y_pred = (y_proba >= umbral_modelo).astype(int)

                acc = accuracy_score(y_real, y_pred)
                prec = precision_score(y_real, y_pred, zero_division=0)
                rec = recall_score(y_real, y_pred, zero_division=0)
                f1 = f1_score(y_real, y_pred, zero_division=0)

                cols_metricas = st.columns(4)
                metricas_vals = [
                    ("Accuracy", f"{acc:.2%}", "#6366f1"),
                    ("Precision", f"{prec:.2%}", "#3b82f6"),
                    ("Recall", f"{rec:.2%}", "#10b981"),
                    ("F1-Score", f"{f1:.2%}", "#e94560"),
                ]
                for i, (nombre, valor, color) in enumerate(metricas_vals):
                    with cols_metricas[i]:
                        st.markdown(
                            f"""
                        <div class="kpi-card">
                            <div class="kpi-value" style="color: {color};">{valor}</div>
                            <div class="kpi-label">{nombre}</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                col_cm, col_roc = st.columns([1, 1])
                with col_cm:
                    st.markdown("#### Matriz de Confusion")
                    fig_cm = crear_matriz_confusion_plot(y_real, y_pred)
                    st.plotly_chart(fig_cm, use_container_width=True, key="cm_modelo")

                with col_roc:
                    st.markdown("#### Curva ROC")
                    fig_roc = crear_curva_roc_plot(y_real, y_proba)
                    st.plotly_chart(fig_roc, use_container_width=True, key="roc_modelo")

                with st.expander("Reporte de clasificacion detallado"):
                    reporte = classification_report(y_real, y_pred, target_names=["Minorista", "Mayorista"], output_dict=True)
                    st.dataframe(pd.DataFrame(reporte).transpose(), use_container_width=True)
            else:
                st.warning("El dataset seleccionado no tiene columna 'clase_real'. No se pueden calcular metricas.")
        else:
            st.warning("Archivo no encontrado.")
    else:
        st.info("Seleccione un dataset con columna 'clase_real' en la barra lateral para ver metricas de rendimiento (accuracy, precision, recall, F1, matriz de confusion, curva ROC).")

# ===========================================================================
# ===========================================================================
# MODULO 4: ESCENARIOS WHAT-IF
# ===========================================================================
# ===========================================================================
elif pagina == "Escenarios What-If":
    st.sidebar.markdown(
        """
<div style="text-align: center; padding-bottom: 0.5rem;">
    <h3 style="color: #1e293b; margin: 0;">Simulador What-If</h3>
    <p style="color: #6b7280; font-size: 0.78rem;">Explore como cambian las predicciones</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    st.sidebar.markdown("#### Modo de analisis")
    modo_whatif = st.sidebar.radio(
        "Seleccione tipo de analisis",
        ["Sliders en Tiempo Real", "Curva de Sensibilidad", "Comparador A/B"],
        key="modo_whatif",
        label_visibility="visible",
    )

    st.sidebar.markdown("---")

    # --- Sliders en Tiempo Real ---
    if modo_whatif == "Sliders en Tiempo Real":
        st.sidebar.markdown("#### Ajuste los parametros")
        kg_whatif = st.sidebar.slider("Cantidad (kg)", 1, 500, 100, 5, key="kg_whatif")
        precio_whatif = st.sidebar.slider("Precio Unitario ($)", 0.0, 500.0, 10.0, 0.5, key="precio_whatif")
        desc_whatif = st.sidebar.slider("Descuento (%)", 0, 100, 10, 1, key="desc_whatif")

        st.markdown('<p class="section-title">Prediccion en Tiempo Real</p>', unsafe_allow_html=True)
        st.caption("La prediccion se actualiza automaticamente al mover cualquier slider.")

        if modelo_cargado:
            df_wi = construir_dataframe(kg_whatif, precio_whatif, desc_whatif)
            clase_wi = modelo.predict(df_wi)[0]
            probs_wi = modelo.predict_proba(df_wi)[0]
            prob_may_wi = probs_wi[1]
            prob_min_wi = probs_wi[0]
            tier_wi = obtener_tier_confianza(prob_may_wi if clase_wi == 1 else prob_min_wi)

            # Resultado principal
            css_wi = "mayorista" if clase_wi == 1 else "minorista"
            texto_wi = "MAYORISTA" if clase_wi == 1 else "MINORISTA"
            color_tier = {"Alta": "#10b981", "Media": "#f59e0b", "Baja": "#ef4444"}[tier_wi]

            col_res, col_gau = st.columns([1, 1])
            with col_res:
                st.markdown(
                    f"""
                <div class="result-card {css_wi}">
                    <div style="font-size: 0.85rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px;">
                        Clasificacion
                    </div>
                    <div class="prediction-label {css_wi}">{texto_wi}</div>
                    <div style="font-size: 0.95rem; color: #6b7280;">
                        Confianza: <strong style="color:{color_tier}">{prob_may_wi if clase_wi == 1 else prob_min_wi:.1%}</strong>
                        <span class="confidence-badge {tier_wi.lower()}" style="margin-left:0.5rem;">{tier_wi}</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col_gau:
                prob_conf_wi = prob_may_wi if clase_wi == 1 else prob_min_wi
                fig_gauge_wi = crear_gauge_confianza(prob_conf_wi)
                st.plotly_chart(fig_gauge_wi, use_container_width=True, key="gauge_whatif")

            # Metricas
            col1w, col2w, col3w = st.columns(3)
            with col1w:
                st.markdown(f"""<div class="metric-box"><div class="value">{prob_may_wi:.1%}</div><div class="label">Prob. Mayorista</div></div>""", unsafe_allow_html=True)
            with col2w:
                st.markdown(f"""<div class="metric-box"><div class="value">{prob_min_wi:.1%}</div><div class="label">Prob. Minorista</div></div>""", unsafe_allow_html=True)
            with col3w:
                importe_wi = kg_whatif * precio_whatif * (1 - desc_whatif / 100)
                st.markdown(f"""<div class="metric-box"><div class="value">${importe_wi:,.2f}</div><div class="label">Importe Total</div></div>""", unsafe_allow_html=True)

            # Barras
            st.plotly_chart(crear_barras_probabilidades(prob_may_wi, prob_min_wi), use_container_width=True, key="barras_whatif")

            # Waterfall
            st.markdown("#### Contribucion de variables")
            fig_wi_waterfall = crear_feature_contribucion_waterfall(
                [kg_whatif, precio_whatif, desc_whatif], FEATURE_IMPORTANCES, COLUMNAS_MODELO, clase_wi
            )
            st.plotly_chart(fig_wi_waterfall, use_container_width=True, key="waterfall_whatif")
        else:
            st.error("Modelo no disponible.")

    # --- Curva de Sensibilidad ---
    elif modo_whatif == "Curva de Sensibilidad":
        st.sidebar.markdown("#### Configuracion de la curva")

        feature_var = st.sidebar.selectbox("Feature a variar", COLUMNAS_MODELO, key="feature_var_sens")

        if feature_var == "cantidad_kg":
            rango_min = st.sidebar.number_input("Min", 1, 500, 1, key="sens_min")
            rango_max = st.sidebar.number_input("Max", 1, 500, 500, key="sens_max")
            default_otros = {"precio_unitario": 10.0, "descuento_pct": 10.0}
        elif feature_var == "precio_unitario":
            rango_min = st.sidebar.number_input("Min", 0.01, 500.0, 0.5, key="sens_min")
            rango_max = st.sidebar.number_input("Max", 0.01, 500.0, 200.0, key="sens_max")
            default_otros = {"cantidad_kg": 100.0, "descuento_pct": 10.0}
        else:
            rango_min = st.sidebar.number_input("Min", 0, 100, 0, key="sens_min")
            rango_max = st.sidebar.number_input("Max", 0, 100, 100, key="sens_max")
            default_otros = {"cantidad_kg": 100.0, "precio_unitario": 10.0}

        st.sidebar.markdown("#### Valores fijos de otras features")
        valores_fijos = {}
        for fn in COLUMNAS_MODELO:
            if fn != feature_var:
                if fn == "descuento_pct":
                    valores_fijos[fn] = st.sidebar.number_input(
                        f"{fn}", 0, 100, int(default_otros[fn]), key=f"sens_fijo_{fn}"
                    )
                else:
                    valores_fijos[fn] = st.sidebar.number_input(
                        f"{fn}", 0.01 if fn == "precio_unitario" else 0.0, 500.0, default_otros[fn],
                        key=f"sens_fijo_{fn}"
                    )

        st.markdown('<p class="section-title">Curva de Sensibilidad</p>', unsafe_allow_html=True)
        st.caption(f"Como cambia la probabilidad de Mayorista al variar **{feature_var}**, manteniendo las demas variables fijas.")

        if modelo_cargado:
            rango = np.linspace(rango_min, rango_max, 100)
            fig_sens = crear_curva_sensibilidad_plot(modelo, COLUMNAS_MODELO, feature_var, rango, valores_fijos)
            st.plotly_chart(fig_sens, use_container_width=True, key="curva_sensibilidad")

            # Tabla de puntos clave
            st.markdown("#### Puntos clave de la curva")
            puntos_clave = []
            for pct in [0.1, 0.3, 0.5, 0.7, 0.9]:
                X_check = []
                for fn in COLUMNAS_MODELO:
                    if fn == feature_var:
                        val = rango_min + pct * (rango_max - rango_min)
                        X_check.append(val)
                    else:
                        X_check.append(valores_fijos.get(fn, 0))
                X_arr = np.array([X_check])
                prob_punto = modelo.predict_proba(X_arr)[0, 1]
                puntos_clave.append({"Feature": f"{int(val) if feature_var != 'precio_unitario' else f'{val:.2f}'}", "P(Mayorista)": f"{prob_punto:.1%}"})

            st.dataframe(pd.DataFrame(puntos_clave), use_container_width=True, hide_index=True)

            # Interpretacion
            st.markdown("#### Interpretacion")
            # Encontrar punto de cruce (umbral 50%)
            X_full = []
            for fn in COLUMNAS_MODELO:
                if fn == feature_var:
                    X_full.append(rango)
                else:
                    X_full.append(np.full_like(rango, valores_fijos.get(fn, 0)))
            X_mat = np.column_stack(X_full)
            probs_full = modelo.predict_proba(X_mat)[:, 1]
            cruce_idx = np.argmax(probs_full >= 0.5) if np.any(probs_full >= 0.5) else -1

            if cruce_idx > 0:
                valor_cruce = rango[cruce_idx]
                st.info(f"El modelo cruza el umbral del 50% (pasa de Minorista a Mayorista) cuando **{feature_var}** alcanza aproximadamente **{valor_cruce:.1f}**.")
            elif np.all(probs_full >= 0.5):
                st.info(f"Con los valores fijos actuales, el modelo siempre predice **Mayorista** en todo el rango de **{feature_var}**.")
            else:
                st.info(f"Con los valores fijos actuales, el modelo siempre predice **Minorista** en todo el rango de **{feature_var}**.")
        else:
            st.error("Modelo no disponible.")

    # --- Comparador A/B ---
    elif modo_whatif == "Comparador A/B":
        st.sidebar.markdown("#### Escenario A")
        kg_a = st.sidebar.slider("Cantidad (kg)", 1, 500, 100, 5, key="kg_a")
        precio_a = st.sidebar.slider("Precio Unitario ($)", 0.0, 500.0, 10.0, 0.5, key="precio_a")
        desc_a = st.sidebar.slider("Descuento (%)", 0, 100, 10, 1, key="desc_a")

        st.sidebar.markdown("---")
        st.sidebar.markdown("#### Escenario B")
        kg_b = st.sidebar.slider("Cantidad (kg)", 1, 500, 300, 5, key="kg_b")
        precio_b = st.sidebar.slider("Precio Unitario ($)", 0.0, 500.0, 8.0, 0.5, key="precio_b")
        desc_b = st.sidebar.slider("Descuento (%)", 0, 100, 20, 1, key="desc_b")

        st.markdown('<p class="section-title">Comparador de Escenarios A/B</p>', unsafe_allow_html=True)
        st.caption("Compare dos escenarios lado a lado para entender como cambian los parametros la clasificacion.")

        if modelo_cargado:
            def predecir_escenario(kg, precio, desc):
                df = construir_dataframe(kg, precio, desc)
                clase = modelo.predict(df)[0]
                probs = modelo.predict_proba(df)[0]
                importe = kg * precio * (1 - desc / 100)
                return {
                    "clase": clase,
                    "etiqueta": MAPA_CLASES[clase],
                    "prob_may": probs[1],
                    "prob_min": probs[0],
                    "confianza": probs[1] if clase == 1 else probs[0],
                    "tier": obtener_tier_confianza(probs[1] if clase == 1 else probs[0]),
                    "importe": importe,
                }

            res_a = predecir_escenario(kg_a, precio_a, desc_a)
            res_b = predecir_escenario(kg_b, precio_b, desc_b)

            col_a, col_vs, col_b = st.columns([4, 1, 4])

            def render_escenario(col, res, kg, precio, desc, label):
                css_cl = "mayorista" if res["clase"] == 1 else "minorista"
                texto_cl = "MAYORISTA" if res["clase"] == 1 else "MINORISTA"
                col.markdown(f"#### Escenario {label}")
                col.markdown(
                    f"""
                <div class="result-card {css_cl}">
                    <div class="prediction-label {css_cl}" style="font-size:2rem;">{texto_cl}</div>
                    <div style="font-size:0.9rem; color:#6b7280;">Confianza: {res['confianza']:.1%} ({res['tier']})</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
                col.markdown(f"**Parametros:** {kg} kg | ${precio:.2f} | {desc}% desc.")
                col.metric("Prob. Mayorista", f"{res['prob_may']:.1%}")
                col.metric("Prob. Minorista", f"{res['prob_min']:.1%}")
                col.metric("Importe Total", f"${res['importe']:,.2f}")

            with col_a:
                render_escenario(col_a, res_a, kg_a, precio_a, desc_a, "A")
            with col_vs:
                st.markdown("<div style='text-align:center; padding-top:6rem; font-size:2rem; font-weight:800; color:#94a3b8;'>VS</div>", unsafe_allow_html=True)
            with col_b:
                render_escenario(col_b, res_b, kg_b, precio_b, desc_b, "B")

            # Resumen de diferencias
            st.markdown("---")
            st.markdown("#### Diferencias entre escenarios")
            diffs = []
            for fn in COLUMNAS_MODELO:
                va = locals()[f"{fn.split('_')[0] if '_' not in fn else fn[:4]}_a"] if f"{fn.split('_')[0] if '_' not in fn else fn[:4]}_a" in locals() else 0
            # Reconstruir diferencias manualmente
            params_labels = [("Cantidad (kg)", kg_a, kg_b), ("Precio Unitario ($)", precio_a, precio_b), ("Descuento (%)", desc_a, desc_b)]
            for label, va, vb in params_labels:
                delta = vb - va
                diffs.append({"Parametro": label, "Escenario A": f"{va:.1f}", "Escenario B": f"{vb:.1f}", "Diferencia": f"{delta:+.1f}"})

            diffs.append({"Parametro": "Importe Total ($)", "Escenario A": f"{res_a['importe']:,.2f}",
                          "Escenario B": f"{res_b['importe']:,.2f}",
                          "Diferencia": f"${res_b['importe'] - res_a['importe']:+,.2f}"})
            diffs.append({"Parametro": "P(Mayorista)", "Escenario A": f"{res_a['prob_may']:.1%}",
                          "Escenario B": f"{res_b['prob_may']:.1%}",
                          "Diferencia": f"{res_b['prob_may'] - res_a['prob_may']:+.1%}"})
            diffs.append({"Parametro": "Clasificacion", "Escenario A": res_a["etiqueta"],
                          "Escenario B": res_b["etiqueta"],
                          "Diferencia": "Cambio" if res_a["clase"] != res_b["clase"] else "Sin cambio"})

            st.dataframe(pd.DataFrame(diffs), use_container_width=True, hide_index=True)

            # Grafico comparativo de barras
            fig_comp = go.Figure(data=[
                go.Bar(name="Escenario A", x=["P(Mayorista)", "P(Minorista)"],
                       y=[res_a["prob_may"], res_a["prob_min"]],
                       marker_color="#e94560", opacity=0.75,
                       text=[f"{res_a['prob_may']:.0%}", f"{res_a['prob_min']:.0%}"], textposition="outside"),
                go.Bar(name="Escenario B", x=["P(Mayorista)", "P(Minorista)"],
                       y=[res_b["prob_may"], res_b["prob_min"]],
                       marker_color="#3b82f6", opacity=0.75,
                       text=[f"{res_b['prob_may']:.0%}", f"{res_b['prob_min']:.0%}"], textposition="outside"),
            ])
            fig_comp.update_layout(barmode="group", height=300, plot_bgcolor="white",
                                    yaxis=dict(ticksuffix="%", range=[0, 1.1], tickformat=".0%"),
                                    legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig_comp, use_container_width=True, key="comparador_ab_barras")
        else:
            st.error("Modelo no disponible.")

# ===========================================================================
# Footer
# ===========================================================================
st.markdown(
    """
<div class="footer">
    Clasificador Retail Inteligente | Modelo RandomForest entrenado con datos sinteticos de retail<br>
    <strong>Aviso:</strong> Las predicciones de este modelo deben usarse como herramienta de apoyo,
    no como unica fuente de decision comercial. | Modulos: Individual &bull; Lote &bull; Analisis &bull; What-If
</div>
""",
    unsafe_allow_html=True,
)
