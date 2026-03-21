import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px
import requests
from google import genai

# --- 🛠️ CONFIGURACIÓN DE RUTAS UNIVERSALES (EL SECRETO DEL CLOUD) ---
# Esto detecta automáticamente si estás en Windows o en la Nube de Streamlit
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_JSON = os.path.join(BASE_DIR, "usuarios.json")

# --- 🛡️ FUNCIÓN DE SEGURIDAD ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🛡️ Acceso Restringido")
        st.text_input("Clave de Acceso NASA:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Clave incorrecta. Reintenta:", type="password", on_change=password_entered, key="password")
        st.error("😕 Acceso denegado.")
        return False
    return True

if not check_password():
    st.stop()

# --- 🎨 CONFIGURACIÓN ÉLITE ---
st.set_page_config(page_title="Arquitecto Jesús | Data Studio", page_icon="📐", layout="wide")

# Estilo NASA Control Center
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1c23 0%, #0e1117 100%); }
    h1, h2, h3 { color: #00FFAA; text-shadow: 0px 0px 10px rgba(0, 255, 170, 0.5); }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 170, 0.3);
        border-radius: 10px; padding: 15px;
    }
    .stButton>button {
        border: 1px solid #00FFAA !important; background-color: transparent !important;
        color: #00FFAA !important; font-weight: bold; transition: all 0.4s ease;
    }
    .stButton>button:hover { background-color: #00FFAA !important; color: #0e1117 !important; box-shadow: 0px 0px 20px #00FFAA; }
    </style>
    """, unsafe_allow_html=True)

# --- 📂 MOTOR DE DATOS (CON RUTA DINÁMICA) ---
def cargar_datos():
    if not os.path.exists(PATH_JSON):
        return []
    try:
        with open(PATH_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []

datos = cargar_datos()
df = pd.DataFrame(datos)

iconos_categorias = {
    "Arquitectura": "🏛️",
    "Ingeniería": "🏗️",
    "Diseño": "🎨",
    "Sistemas": "💻"
}

# --- ⚙️ SIDEBAR (PANEL DE CONTROL) ---
with st.sidebar:
    st.markdown("### `SYS_STATUS: ONLINE` ✅")
    st.title("⚙️ Panel de Control")
    api_key_input = st.text_input("🔑 Google API Key:", type="password")
    st.divider()

    if not df.empty:
        opciones = ["Todos"] + list(df['categoria'].unique())
        seleccion = st.selectbox("Filtrar Categoría:", opciones)
        
        df_filtrado = df.copy()
        if seleccion != "Todos":
            df_filtrado = df[df['categoria'] == seleccion]

    st.subheader("📥 Importar Datos")
    archivo_subido = st.file_uploader("Arrastra un JSON", type=["json"])
    if archivo_subido and st.button("🔄 Actualizar Base"):
        try:
            nuevos_datos = json.load(archivo_subido)
            with open(PATH_JSON, "w", encoding="utf-8") as f:
                json.dump(nuevos_datos, f, indent=4, ensure_ascii=False)
            st.success("¡Base actualizada!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# --- 🌐 VISTA PRINCIPAL ---
if not df.empty:
    st.title("🌐 Sistema Gestión de Personal Dinámico")

    # A. GESTIÓN DE USUARIOS (CRUD)
    # --- 🏢 CONSOLA DE ADMINISTRACIÓN GLOBAL ---
    with st.expander("⚙️ Gestión Avanzada de Personal y Categorías"):
        
        tab1, tab2, tab3 = st.tabs(["👤 Editar/Eliminar", "➕ Nuevo Usuario", "📁 Gestionar Áreas"])

        # TAB 1: EDITAR O ELIMINAR EXISTENTES
        with tab1:
            nombres = df['nombre'].tolist()
            user_sel = st.selectbox("Seleccionar empleado para modificar:", nombres)
            idx = df.index[df['nombre'] == user_sel][0]
            
            c1, c2 = st.columns(2)
            n_edad = c1.number_input("Nueva Edad:", value=int(df.at[idx, 'edad']), key="edit_age")
            
            # Categorías dinámicas: las saca del propio DF o de una lista guardada
            cats_existentes = list(df['categoria'].unique())
            n_cat = c2.selectbox("Cambiar Área:", cats_existentes, index=cats_existentes.index(df.at[idx, 'categoria']))

            col_btns = st.columns(2)
            if col_btns[0].button("💾 Actualizar Datos", use_container_width=True):
                df.at[idx, 'edad'] = n_edad
                df.at[idx, 'categoria'] = n_cat
                with open(PATH_JSON, "w", encoding="utf-8") as f:
                    json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
                st.success(f"¡{user_sel} actualizado!"); st.rerun()
            
            if col_btns[1].button("🗑️ ELIMINAR EMPLEADO", type="primary", use_container_width=True):
                df = df.drop(idx)
                with open(PATH_JSON, "w", encoding="utf-8") as f:
                    json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
                st.warning(f"Usuario eliminado."); st.rerun()

        # TAB 2: AÑADIR NUEVO (ESCALABILIDAD)
        with tab2:
            st.markdown("### Registrar nuevo integrante")
            with st.form("nuevo_user"):
                new_nom = st.text_input("Nombre Completo:", key="input_nuevo_nombre")
                new_ed = st.number_input("Edad:", min_value=18, max_value=90)
                new_ca = st.selectbox("Asignar a Área:", list(df['categoria'].unique()))
                if st.form_submit_button("🚀 Dar de Alta"):
                    nuevo_registro = {"nombre": new_nom, "edad": new_ed, "categoria": new_ca}
                    datos.append(nuevo_registro)
                    with open(PATH_JSON, "w", encoding="utf-8") as f:
                        json.dump(datos, f, indent=4, ensure_ascii=False)
                    st.success("Registrado correctamente"); st.rerun()

    
        # TAB 3: GESTIONAR ÁREAS (EL CORAZÓN DEL SaaS)
        with tab3:
            st.markdown("### Configuración de la Organización")
            # Añadimos key="area_admin_input" para que sea único
            nueva_area = st.text_input("Nombre de la nueva Área:", key="area_admin_input") 
            if st.button("🆕 Crear Nueva Área", key="btn_crear_area"):
                st.info(f"Área '{nueva_area}' lista para ser asignada.")


    # B. CONSULTOR GEMINI 3 FLASH (ELITE)
    st.divider()
    st.subheader("🤖 Consultor Senior Gemini 3 Flash")
    
    if api_key_input:
        if st.button("🧠 GENERAR DIAGNÓSTICO ÉLITE"):
            try:
                client = genai.Client(api_key=api_key_input)
                datos_ia = df_filtrado[['nombre', 'edad', 'categoria']].to_string()
                
                with st.spinner("Conectando con el cerebro de Google v3..."):
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=f"Analiza este equipo y da 3 consejos: {datos_ia}"
                    )
                    st.info("📋 Informe Estratégico:")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error de IA: {e}")
    else:
        st.info("Introduce tu API Key para activar la IA.")

    # C. MÉTRICAS Y GRÁFICOS
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Personal", len(df_filtrado))
    m2.metric("Edad Promedio", f"{df_filtrado['edad'].mean():.1f}")
    m3.metric("Filtro Activo", seleccion)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_pie = px.pie(df_filtrado, values='edad', names='categoria', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_b:
        st.bar_chart(df_filtrado.set_index("nombre")["edad"], color="#00FFAA")

else:
    st.title("🌐 Sistema Gestion de Personal")
    st.warning("⚠️ No hay datos. Sube un archivo JSON en el panel lateral.")