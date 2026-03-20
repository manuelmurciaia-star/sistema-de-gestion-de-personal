import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px
import requests
from google import genai

# --- FUNCIÓN DE SEGURIDAD (EL GUARDIÁN) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🛡️ Acceso Restringido")
        st.text_input("Clave NASA:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Clave incorrecta:", type="password", on_change=password_entered, key="password")
        st.error("😕 Acceso denegado.")
        return False
    return True

if not check_password():
    st.stop()

# 1. CONFIGURACIÓN Y ESTILO NASA
st.set_page_config(page_title="Arquitecto Jesús | Studio", page_icon="📐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c23 0%, #0e1117 100%); }
    h1 { color: #00FFAA; text-shadow: 0px 0px 10px rgba(0, 255, 170, 0.5); letter-spacing: 2px; }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 170, 0.3);
        border-radius: 10px; padding: 15px;
    }
    .stButton>button {
        border: 1px solid #00FFAA !important; background: transparent !important; color: #00FFAA !important;
    }
    .stButton>button:hover { background: #00FFAA !important; color: black !important; box-shadow: 0px 0px 20px #00FFAA; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE DATOS
def cargar_datos():
    try:
        with open("src/usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

df = pd.DataFrame(cargar_datos())
iconos_categorias = {
    "Seguros Vida": "🛡️",
    "Seguros Auto": "🚗",
    "Seguros Hogar": "🏠",
    "Inversiones": "📈"
}

# 3. SIDEBAR (CONFIGURACIÓN)
with st.sidebar:
    st.markdown("### `SYS_STATUS: ONLINE` ✅")
    st.title("⚙️ Panel de Control")
    api_key_input = st.text_input("🔑 Google API Key:", type="password", help="Pega aquí tu clave de AI Studio")
    st.divider()
    
    if not df.empty:
        opciones = ["Todos"] + list(df['categoria'].unique())
        seleccion = st.selectbox("Filtrar Categoría:", opciones)
        df_filtrado = df if seleccion == "Todos" else df[df['categoria'] == seleccion]
    
    st.subheader("📥 Importar Datos")
    archivo = st.file_uploader("Subir JSON", type=["json"])
    if archivo and st.button("🔄 Actualizar Base"):
        with open("src/usuarios.json", "w", encoding="utf-8") as f:
            json.dump(json.load(archivo), f, indent=4, ensure_ascii=False)
        st.rerun()

# 4. CUERPO PRINCIPAL
if not df.empty:
    st.title("🌐 SISTEMA GESTIÓN DE EMPLEADOS")

    # A. CENTINELA
    with st.expander("🛡️ Auditoría del Centinela", expanded=False):
        corruptos = df[(df['edad'] <= 0) | (df['nombre'] == "")]
        if not corruptos.empty: st.error(f"🚨 {len(corruptos)} registros corruptos.")
        vacias = [c for c in iconos_categorias.keys() if c not in df['categoria'].unique()]
        if vacias: st.warning(f"⚠️ Falta talento en: {', '.join(vacias)}")

    # B. CRUD
    busqueda = st.text_input("🔍 Buscar por nombre:", placeholder="Escribe para filtrar...")
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado['nombre'].str.contains(busqueda, case=False)]

    with st.expander("📝 Gestión de Usuarios"):
        nombres = df['nombre'].tolist()
        user_sel = st.selectbox("Selecciona un usuario:", nombres)
        idx = df.index[df['nombre'] == user_sel][0]
        fila = df.loc[idx]

        c1, c2 = st.columns(2)
        with c1:
            n_edad = st.number_input("Edad:", value=int(fila['edad']), key="e_age")
        
        with c2:
            # --- AQUÍ ESTÁ EL BLOQUE NUEVO BIEN ALINEADO ---
            lista_opciones = list(iconos_categorias.keys())
            categoria_actual = df.loc[idx, 'categoria']

            if categoria_actual in lista_opciones:
                indice_por_defecto = lista_opciones.index(categoria_actual)
            else:
                indice_por_defecto = 0

            n_cat = st.selectbox("Categoría:", lista_opciones, index=indice_por_defecto)
        
        if st.button("💾 Guardar Cambios"):
            df.at[idx, 'edad'], df.at[idx, 'categoria'] = n_edad, n_cat
            with open("src/usuarios.json", "w", encoding="utf-8") as f:
                json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
            st.success("OK"); st.rerun()

    # C. INTELIGENCIA ARTIFICIAL (GEMINiS)

# --- 🤖 CONSULTOR SENIOR GEMINI 3 (ELITE 2026) ---
    st.divider()
    st.subheader("🤖 Consultor Estratégico Gemini 3 Flash")

    if api_key_input:
        try:
            # 1. Inicialización según documentación oficial
            client = genai.Client(api_key=api_key_input)

            if st.button("🧠 GENERAR DIAGNÓSTICO DE NUEVA GENERACIÓN"):
                datos_ia = df_filtrado[['nombre', 'edad', 'categoria']].to_string()
                
                with st.spinner("Conectando con Gemini 3 Flash Preview..."):
                    # 2. Llamada al modelo de vanguardia que encontraste
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents= f"Actúa como un Gerente de Ventas Senior. Analiza el rendimiento de estos vendedores y dime quién merece un bono: {datos_ia}"
                    )
                    
                    st.write("---")
                    st.success("✅ ¡CONEXIÓN EXITOSA CON GEMINI 3!")
                    # 3. Impresión del resultado
                    st.markdown(response.text)
                    
        except Exception as e:
            st.error(f"❌ Error de última generación: {e}")
            st.info("Verifica que tu API Key sea de Google AI Studio v3.")
    else:
        st.info("Introduce la API Key en el sidebar.")

    # D. BI & MÉTRICAS
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Personal", len(df_filtrado))
    col2.metric("Edad Media", f"{df_filtrado['edad'].mean():.1f}")
    col3.metric("Filtro", seleccion if 'seleccion' in locals() else "Todos")

    ca, cb = st.columns(2)
    with ca:
        fig = px.pie(df_filtrado, names='categoria', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        st.bar_chart(df_filtrado.set_index("nombre")["edad"], color="#00FFAA")

else:
    st.title("🌐 Sistema NASA")
    st.warning("Sin datos. Sube un JSON en el panel lateral.")