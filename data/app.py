
import json
from pathlib import Path

import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Candy Market",
    page_icon="💄",
    layout="wide"
)

# Archivo donde se guardan los productos
CARPETA_DATOS = Path("data")
ARCHIVO_DATOS = CARPETA_DATOS / "productos.json"

# Categorías del catálogo
CATEGORIAS = [
    "Cuidado facial",
    "Cuidado capilar",
    "Maquillaje",
    "Perfumería",
    "Cuidado corporal",
    "Higiene personal"
]

# Productos iniciales
PRODUCTOS_INICIALES = [
    {"codigo": "BC001", "nombre": "Crema Hidratante Facial", "categoria": "Cuidado facial", "precio": 45900, "stock": 15, "descripcion": "Crema para hidratar y cuidar la piel del rostro."},
    {"codigo": "BC002", "nombre": "Serum de Vitamina C", "categoria": "Cuidado facial", "precio": 59900, "stock": 8, "descripcion": "Producto para el cuidado diario de la piel."},
    {"codigo": "BC003", "nombre": "Agua Micelar", "categoria": "Cuidado facial", "precio": 32900, "stock": 20, "descripcion": "Ayuda a limpiar el rostro y retirar el maquillaje."},
    {"codigo": "BC004", "nombre": "Champú Hidratante", "categoria": "Cuidado capilar", "precio": 29900, "stock": 25, "descripcion": "Champú para la limpieza e hidratación del cabello."},
    {"codigo": "BC005", "nombre": "Mascarilla Capilar", "categoria": "Cuidado capilar", "precio": 42900, "stock": 10, "descripcion": "Tratamiento para ayudar a suavizar el cabello."},
    {"codigo": "BC006", "nombre": "Labial Mate", "categoria": "Maquillaje", "precio": 25900, "stock": 30, "descripcion": "Labial de acabado mate para uso diario."},
    {"codigo": "BC007", "nombre": "Pestañina Negra", "categoria": "Maquillaje", "precio": 34900, "stock": 16, "descripcion": "Producto de maquillaje para las pestañas."},
    {"codigo": "BC008", "nombre": "Perfume Floral", "categoria": "Perfumería", "precio": 119900, "stock": 9, "descripcion": "Fragancia con aroma floral."},
    {"codigo": "BC009", "nombre": "Crema Corporal", "categoria": "Cuidado corporal", "precio": 38900, "stock": 22, "descripcion": "Crema para hidratar la piel del cuerpo."},
    {"codigo": "BC010", "nombre": "Jabón Líquido", "categoria": "Higiene personal", "precio": 19900, "stock": 0, "descripcion": "Jabón líquido para la higiene diaria."}
]


def guardar_productos(productos):
    """Guarda los productos en un archivo JSON."""
    CARPETA_DATOS.mkdir(exist_ok=True)
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, ensure_ascii=False, indent=4)


def cargar_productos():
    """Carga los productos o crea los iniciales."""
    CARPETA_DATOS.mkdir(exist_ok=True)

    if not ARCHIVO_DATOS.exists():
        guardar_productos(PRODUCTOS_INICIALES)
        return PRODUCTOS_INICIALES.copy()

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        st.error("No fue posible leer el archivo de productos.")
        return []


def estado_stock(stock):
    if stock <= 0:
        return "Sin stock"
    elif stock < 10:
        return "Stock bajo"
    return "Disponible"


def formato_pesos(valor):
    return "$" + format(int(valor), ",").replace(",", ".")


# ==========================================
# ESTILOS DE LA PÁGINA
# ==========================================

st.markdown("""
<style>

    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #f4f8ff 55%,
            #f1fff9 100%
        );
    }

    .main .block-container {
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }

    /* ENCABEZADO */

    .hero {
        background: linear-gradient(
            110deg,
            #8e44ad 0%,
            #e84393 48%,
            #ff8a65 100%
        );
        padding: 30px 24px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(180, 65, 140, 0.20);
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin: 0;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .hero p {
        color: #fff5fb;
        font-size: 16px;
        margin: 8px 0 0 0;
    }

    /* TÍTULOS */

    .section-title {
        color: #813c83;
        font-weight: 800;
        font-size: 23px;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    /* TARJETAS KPI */

    .kpi-card {
        background: white;
        border-radius: 17px;
        padding: 18px 18px 16px 18px;
        min-height: 118px;
        border: 1px solid #f4ddeb;
        box-shadow: 0 5px 18px rgba(119, 69, 115, 0.09);
    }

    .kpi-label {
        color: #777080;
        font-size: 13px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #7d3c83;
        font-size: 27px;
        font-weight: 800;
        line-height: 1.2;
    }

    .kpi-note {
        color: #a19aaa;
        font-size: 11px;
        margin-top: 6px;
    }

    /* ==================================
       BOTONES PEQUEÑOS CON DEGRADADO
       ================================== */

    div.stButton > button,
    div.stFormSubmitButton > button {

        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;

        font-size: 13px !important;
        font-weight: 800 !important;

        padding: 5px 16px !important;

        height: 36px !important;
        min-height: 36px !important;

        width: auto !important;
        min-width: 100px !important;

        background: linear-gradient(
            100deg,
            #8e44ad,
            #e84393,
            #ff8a65
        ) !important;

        box-shadow: 0 3px 9px rgba(204, 70, 150, 0.22) !important;

        transition: all 0.2s ease-in-out;
    }

    div.stButton > button *,
    div.stFormSubmitButton > button * {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* EFECTO AL PASAR EL MOUSE */

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {

        color: white !important;
        border: none !important;

        transform: translateY(-2px);

        box-shadow: 0 7px 16px rgba(204, 70, 150, 0.30) !important;
    }

    /* BOTONES DESHABILITADOS */

    div.stButton > button:disabled,
    div.stFormSubmitButton > button:disabled {

        background: #d8cbd8 !important;
        color: white !important;
        box-shadow: none !important;
    }

    /* FORMULARIOS */

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #f1d9e9;
        border-radius: 16px;
        padding: 18px;
    }

    /* PESTAÑAS */

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #f1d9e9;
        border-radius: 14px;
    }

    /* TABLA */

    div[data-testid="stDataFrame"] {
        border: 1px solid #efd8e8;
        border-radius: 13px;
        overflow: hidden;
    }

    label, .stMarkdown, p {
        color: #51465a;
    }

    hr {
        border-color: #efd8e8;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# CARGAR PRODUCTOS
# ==========================================

if "productos" not in st.session_state:
    st.session_state.productos = cargar_productos()

productos = st.session_state.productos


# ==========================================
# ENCABEZADO PRINCIPAL
# ==========================================

st.markdown("""
<div class="hero">
    <h1>Candy Market</h1>
    <p>Tu belleza, tu esencia, tu brillo · Catálogo e inventario</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# INDICADORES KPI
# ==========================================

total_productos = len(productos)
total_unidades = sum(p["stock"] for p in productos)
valor_inventario = sum(p["precio"] * p["stock"] for p in productos)
productos_bajos = sum(1 for p in productos if p["stock"] < 10)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">PRODUCTOS REGISTRADOS</div>
        <div class="kpi-value">{total_productos}</div>
        <div class="kpi-note">Referencias en el catálogo</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">UNIDADES DISPONIBLES</div>
        <div class="kpi-value">{total_unidades}</div>
        <div class="kpi-note">Unidades en inventario</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">VALOR DEL INVENTARIO</div>
        <div class="kpi-value" style="font-size:23px;">
            {formato_pesos(valor_inventario)}
        </div>
        <div class="kpi-note">Valor calculado según el stock</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">STOCK BAJO O AGOTADO</div>
        <div class="kpi-value">{productos_bajos}</div>
        <div class="kpi-note">Productos que requieren atención</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# REGISTRAR PRODUCTO
# ==========================================

st.write("")
st.markdown(
    '<div class="section-title">Registrar un producto</div>',
    unsafe_allow_html=True
)

with st.form("formulario_nuevo", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        codigo = st.text_input(
            "Código del producto",
            placeholder="Ej. BC011"
        )

        nombre = st.text_input(
            "Nombre del producto",
            placeholder="Nombre del producto"
        )

        categoria = st.selectbox(
            "Categoría",
            CATEGORIAS
        )

    with col2:
        precio = st.number_input(
            "Precio (COP)",
            min_value=0,
            step=1000
        )

        stock = st.number_input(
            "Cantidad en stock",
            min_value=0,
            step=1
        )

        descripcion = st.text_area(
            "Descripción",
            placeholder="Describe brevemente el producto"
        )

    espacio, columna_boton = st.columns([5, 1.35])

    with columna_boton:
        guardar = st.form_submit_button(
            "Crear",
            width="content"
        )


if guardar:

    codigo = codigo.strip().upper()
    nombre = nombre.strip()

    if codigo == "" or nombre == "":
        st.error("Debes escribir el código y el nombre del producto.")

    elif any(p["codigo"].upper() == codigo for p in productos):
        st.error("Ese código ya se encuentra registrado.")

    else:

        nuevo_producto = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": int(precio),
            "stock": int(stock),
            "descripcion": descripcion.strip()
        }

        productos.append(nuevo_producto)

        guardar_productos(productos)

        st.session_state.productos = productos

        st.success("El producto se agregó correctamente.")

        st.rerun()


# ==========================================
# CATÁLOGO DE PRODUCTOS
# ==========================================

st.write("")

st.markdown(
    '<div class="section-title">Catálogo de productos</div>',
    unsafe_allow_html=True
)


# BÚSQUEDA Y FILTROS

col_busqueda, col_categoria, col_estado = st.columns([2, 1, 1])

with col_busqueda:
    busqueda = st.text_input(
        "Buscar producto",
        placeholder="Escribe el código o nombre"
    )

with col_categoria:
    filtro_categoria = st.selectbox(
        "Filtrar por categoría",
        ["Todas"] + CATEGORIAS
    )

with col_estado:
    filtro_estado = st.selectbox(
        "Filtrar por estado",
        ["Todos", "Disponible", "Stock bajo", "Sin stock"]
    )


# ==========================================
# APLICAR FILTROS
# ==========================================

productos_filtrados = []

for producto in productos:

    coincide_texto = (
        busqueda.lower() in producto["codigo"].lower()
        or busqueda.lower() in producto["nombre"].lower()
    )

    coincide_categoria = (
        filtro_categoria == "Todas"
        or producto["categoria"] == filtro_categoria
    )

    coincide_estado = (
        filtro_estado == "Todos"
        or estado_stock(producto["stock"]) == filtro_estado
    )

    if coincide_texto and coincide_categoria and coincide_estado:
        productos_filtrados.append(producto)


# ==========================================
# MOSTRAR TABLA Y SELECCIONAR PRODUCTO
# ==========================================

if productos_filtrados:

    datos_tabla = []

    for producto in productos_filtrados:

        datos_tabla.append({
            "Código": producto["codigo"],
            "Producto": producto["nombre"],
            "Categoría": producto["categoria"],
            "Precio": formato_pesos(producto["precio"]),
            "Stock": producto["stock"],
            "Estado": estado_stock(producto["stock"]),
            "Descripción": producto["descripcion"]
        })

    tabla = pd.DataFrame(datos_tabla)

    st.caption(
        "Haz clic en una fila de la tabla para seleccionar el producto "
        "y habilitar las opciones de edición o eliminación."
    )

    clave_tabla = (
        f"tabla_productos_{busqueda}_{filtro_categoria}_"
        f"{filtro_estado}_{tuple(p['codigo'] for p in productos_filtrados)}"
    )

    evento_tabla = st.dataframe(
        tabla,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=clave_tabla
    )

    filas_seleccionadas = evento_tabla.selection.rows

    if (
        filas_seleccionadas
        and 0 <= filas_seleccionadas[0] < len(productos_filtrados)
    ):

        indice_fila = filas_seleccionadas[0]
        producto_actual = productos_filtrados[indice_fila]

        st.write("")

        st.markdown(
            '<div class="section-title">Acciones del producto seleccionado</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"Producto seleccionado: **{producto_actual['nombre']}** "
            f"· Código: **{producto_actual['codigo']}**"
        )

        tab_editar, tab_eliminar = st.tabs([
            "Editar producto",
            "Eliminar producto"
        ])


        # ==================================
        # EDITAR PRODUCTO
        # ==================================

        with tab_editar:

            with st.form("formulario_editar"):

                col_edit1, col_edit2 = st.columns(2)

                with col_edit1:

                    nuevo_codigo = st.text_input(
                        "Código",
                        value=producto_actual["codigo"]
                    )

                    nuevo_nombre = st.text_input(
                        "Nombre",
                        value=producto_actual["nombre"]
                    )

                    indice_categoria = (
                        CATEGORIAS.index(producto_actual["categoria"])
                        if producto_actual["categoria"] in CATEGORIAS
                        else 0
                    )

                    nueva_categoria = st.selectbox(
                        "Categoría",
                        CATEGORIAS,
                        index=indice_categoria
                    )

                with col_edit2:

                    nuevo_precio = st.number_input(
                        "Precio (COP)",
                        min_value=0,
                        value=int(producto_actual["precio"]),
                        step=1000
                    )

                    nuevo_stock = st.number_input(
                        "Stock",
                        min_value=0,
                        value=int(producto_actual["stock"]),
                        step=1
                    )

                    nueva_descripcion = st.text_area(
                        "Descripción",
                        value=producto_actual["descripcion"]
                    )

                espacio, columna_boton = st.columns([5, 1.35])

                with columna_boton:
                    actualizar = st.form_submit_button(
                        "Guardar",
                        width="content"
                    )

            if actualizar:

                nuevo_codigo = nuevo_codigo.strip().upper()
                nuevo_nombre = nuevo_nombre.strip()

                codigo_repetido = any(
                    p["codigo"].upper() == nuevo_codigo
                    and p["codigo"] != producto_actual["codigo"]
                    for p in productos
                )

                if nuevo_codigo == "" or nuevo_nombre == "":

                    st.error("El código y el nombre son obligatorios.")

                elif codigo_repetido:

                    st.error("Ya existe otro producto con ese código.")

                else:

                    indice_original = productos.index(producto_actual)

                    productos[indice_original] = {
                        "codigo": nuevo_codigo,
                        "nombre": nuevo_nombre,
                        "categoria": nueva_categoria,
                        "precio": int(nuevo_precio),
                        "stock": int(nuevo_stock),
                        "descripcion": nueva_descripcion.strip()
                    }

                    guardar_productos(productos)

                    st.session_state.productos = productos

                    st.success(
                        "Los cambios se guardaron correctamente."
                    )

                    # Actualizar la tabla y limpiar la selección
                    st.session_state["version_tabla"] = (
                        st.session_state.get("version_tabla", 0) + 1
                    )

                    st.rerun()


        # ==================================
        # ELIMINAR PRODUCTO
        # ==================================

        with tab_eliminar:

            st.warning(
                f"Vas a eliminar **{producto_actual['nombre']}**. "
                "Esta acción no se puede deshacer."
            )

            confirmar = st.checkbox(
                "Confirmo que deseo eliminar este producto",
                key="confirmar_eliminar"
            )

            espacio, columna_boton = st.columns([5, 1.35])

            with columna_boton:

                eliminar = st.button(
                    "Eliminar",
                    disabled=not confirmar,
                    width="content"
                )

            if eliminar:

                productos.remove(producto_actual)

                guardar_productos(productos)

                st.session_state.productos = productos

                st.session_state["version_tabla"] = (
                    st.session_state.get("version_tabla", 0) + 1
                )

                st.session_state.pop("confirmar_eliminar", None)

                st.success("El producto fue eliminado.")

                st.rerun()

    else:

        st.info(
            "Selecciona una fila de la tabla para ver las opciones "
            "de editar y eliminar."
        )

else:

    st.info("No se encontraron productos con esos filtros.")


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.write("")

st.caption(
    "Candy Market | Proyecto académico de catálogo de productos"
)
