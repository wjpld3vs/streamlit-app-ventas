# Clasificador Retail Inteligente - Dashboard Streamlit

Aplicacion web local desarrollada con **Streamlit** que utiliza un modelo de **Machine Learning (Random Forest)** para clasificar operaciones de venta retail como **Mayorista** o **Minorista**.

---

## Proposito general del dashboard

Esta herramienta permite a equipos comerciales y de operaciones evaluar rapidamente si una transaccion de compra corresponde a un perfil de **cliente Mayorista** o **cliente Minorista**, basandose en tres variables clave: cantidad de producto, precio unitario y porcentaje de descuento aplicado.

### Que problema resuelve

En entornos retail, distinguir entre clientes mayoristas y minoristas puede ser complejo cuando hay zonas grises (compras de volumen medio, descuentos intermedios). Este dashboard automatiza esa clasificacion usando un modelo entrenado, proporcionando:

- Una clasificacion inmediata basada en datos.
- La probabilidad de pertenencia a cada clase.
- Una interpretacion en lenguaje de negocio para facilitar la toma de decisiones.

---

## Como se conecta Streamlit con el modelo

1. **Carga del modelo**: `app.py` utiliza `joblib` para cargar `modelo_clasificacion_retail.pkl` mediante el decorador `@st.cache_resource`, lo que garantiza que el modelo se cargue una sola vez en memoria.
2. **Entrada de usuario**: Los controles interactivos de Streamlit en la barra lateral capturan los valores de `cantidad_kg`, `precio_unitario` y `descuento_pct`.
3. **Construccion del DataFrame**: Se construye un `pd.DataFrame` con los nombres exactos de columna que espera el modelo (`[cantidad_kg, precio_unitario, descuento_pct]`).
4. **Prediccion**: Se llama a `modelo.predict()` y `modelo.predict_proba()` para obtener la clase y las probabilidades.
5. **Visualizacion**: Los resultados se muestran en tarjetas de metricas, graficos de barras y mensajes interpretativos.

### Tipo de prediccion

Clasificacion binaria supervisada con dos clases:
- `0` → **Minorista**
- `1` → **Mayorista**

---

## Estructura del proyecto

```
proyecto-streamlit-pkl/
├── app.py
├── modelo_clasificacion_retail.pkl
├── requirements.txt
├── README.md
└── docs/
    └── streamlit_componentes.md
```

| Archivo / Carpeta | Descripcion |
|---|---|
| `app.py` | Aplicacion principal de Streamlit con toda la logica de carga, prediccion y visualizacion |
| `modelo_clasificacion_retail.pkl` | Modelo RandomForest entrenado, cargado en la app via joblib |
| `requirements.txt` | Dependencias Python necesarias para ejecutar el proyecto |
| `README.md` | Este archivo de documentacion |
| `docs/streamlit_componentes.md` | Guia detallada de cada componente de Streamlit utilizado |

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

La aplicacion se abrira automaticamente en su navegador en `http://localhost:8501`.

---

## Uso de archivos .pkl en el proyecto

### Como se carga el modelo

```python
import joblib

@st.cache_resource
def cargar_modelo(ruta_modelo: str):
    return joblib.load(ruta_modelo)

modelo = cargar_modelo("modelo_clasificacion_retail.pkl")
```

Se usa `joblib` en lugar de `pickle` porque esta optimizado para objetos grandes de scikit-learn y maneja mejor la serializacion de arrays NumPy.

### Donde ubicar el archivo .pkl

El archivo `modelo_clasificacion_retail.pkl` debe estar en la **raiz del proyecto**, en el mismo directorio que `app.py`.

### Precauciones al trabajar con archivos .pkl

- Solo cargue archivos .pkl de **fuentes confiables** (los archivos pickle pueden ejecutar codigo arbitrario al deserializarse).
- Verifique que la version de scikit-learn usada para guardar el modelo sea **compatible** con la version instalada en su entorno.
- No modifique el archivo .pkl manualmente.
- Si cambia el modelo, asegurese de actualizar las constantes `COLUMNAS_MODELO` y `MAPA_CLASES` en `app.py`.

### Como validar que el modelo fue cargado correctamente

Ejecute el siguiente script de verificacion:

```python
import joblib

modelo = joblib.load("modelo_clasificacion_retail.pkl")
print("Tipo:", type(modelo).__name__)
print("Clases:", modelo.classes_)
print("Features:", modelo.feature_names_in_)
print("predict_proba:", hasattr(modelo, "predict_proba"))
```

Salida esperada:
```
Tipo: RandomForestClassifier
Clases: [0 1]
Features: ['cantidad_kg' 'precio_unitario' 'descuento_pct']
predict_proba: True
```

---

## Flujo de funcionamiento de la app

1. **El usuario introduce valores** en la barra lateral (cantidad_kg, precio_unitario, descuento_pct).
2. **Streamlit construye un DataFrame** con las columnas `['cantidad_kg', 'precio_unitario', 'descuento_pct']` respetando el orden exacto de entrenamiento.
3. **El modelo .pkl genera la prediccion** usando `predict()` y `predict_proba()`.
4. **La app muestra la clase predicha** (Mayorista o Minorista) en una tarjeta destacada.
5. **Se muestran las probabilidades** por clase en formato de metricas numericas.
6. **Se genera una interpretacion** visual (grafico de barras) y textual (mensaje contextual) del resultado.

---

## Prueba de funcionamiento

Para verificar que el modelo responde correctamente, pruebe con estos valores:

| Parametro | Valor |
|---|---|
| cantidad_kg | 400 |
| precio_unitario | 10.00 |
| descuento_pct | 15% |

**Resultado esperado:** Clasificacion como **Mayorista** con probabilidad aproximada de **96%**.

Caso contrario (Minorista):

| Parametro | Valor |
|---|---|
| cantidad_kg | 10 |
| precio_unitario | 5.00 |
| descuento_pct | 0% |

**Resultado esperado:** Clasificacion como **Minorista** con probabilidad aproximada de **94%**.

---

## Documentacion de componentes Streamlit

Consulte [`docs/streamlit_componentes.md`](docs/streamlit_componentes.md) para una guia detallada de cada componente de Streamlit utilizado en el dashboard y como adaptarlos.

---

## Como extender el proyecto

### Agregar nuevas variables

1. Reentrene el modelo con las nuevas variables.
2. Actualice la lista `COLUMNAS_MODELO` en `app.py` con los nombres exactos de las columnas.
3. Agregue nuevos controles de entrada en la barra lateral (`st.number_input`, `st.slider`, etc.).
4. Actualice `construir_dataframe()` para incluir las nuevas variables en el orden correcto.

### Cambiar el modelo

1. Reemplace `modelo_clasificacion_retail.pkl` por el nuevo archivo .pkl.
2. Ejecute el script de verificacion para inspeccionar el nuevo modelo.
3. Actualice `COLUMNAS_MODELO` y `MAPA_CLASES` segun corresponda.
4. Si el nuevo modelo no soporta `predict_proba`, ajuste la visualizacion de probabilidades.

### Agregar graficos adicionales

Streamlit soporta multiples librerias de visualizacion:
- `st.bar_chart` (nativo, como en este proyecto)
- `st.line_chart`, `st.area_chart`, `st.scatter_chart`
- `st.pyplot` para graficos de matplotlib
- `st.plotly_chart` para graficos interactivos de Plotly

---

## Buenas practicas

- **Separacion de responsabilidades**: La carga del modelo, la preparacion de datos y la visualizacion estan en funciones separadas.
- **Cacheo con `@st.cache_resource`**: Evita recargar el modelo en cada interaccion del usuario.
- **Validacion de entradas**: Los controles `st.number_input` y `st.slider` tienen rangos definidos (min/max).
- **Manejo de errores**: Se capturan excepciones si el archivo .pkl no existe o no puede cargarse.
- **Seguridad**: Nunca se cargan archivos .pkl subidos por el usuario. El modelo es fijo y conocido.
- **Nombres de columnas explicitos**: El DataFrame se construye con los nombres exactos requeridos por el modelo.
- **No requiere scaler.pkl**: Random Forest no necesita escalado de variables.
