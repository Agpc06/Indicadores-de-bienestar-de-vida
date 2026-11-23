import streamlit as st

st.set_page_config(
    page_title="Marco Metodológico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica")
st.markdown("---")

st.subheader("Marco Metodológico 📑")
st.markdown("Este apartado detalla el enfoque y camino técnico seguido para el procesamiento y análisis de los datos del World Development Indicators (WDI).")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Enfoque y Diseño 📐")
    st.markdown("""
    *   **Enfoque:** Cuantitativo, basado en el análisis de variables numéricas, estadísticas descriptivas y correlaciones a través del tiempo.
    *   **Diseño:** No experimental, de tipo longitudinal y correlacional. Se observan los fenómenos en su contexto histórico natural sin manipulación experimental de variables.
    """)

with col2:
    st.markdown("### Universo y Muestra 📉")
    st.markdown("""
    *   **Universo Estadístico:** Todos los países que forman parte de la región latinoamericana y el Caribe registrados en el dataset de Indicadores del Desarrollo Mundial (World Bank).
    *   **Muestra:** Selección no probabilística de países de la región que cuentan con series de datos continuas y consistentes para las variables de estudio durante el período **1963 – 2023**.
    """)

st.markdown("---")
st.subheader("Variables e Indicadores Clave")
st.markdown("""
| Dimensión | Indicador | Código BM | Unidad |
| :--- | :--- | :--- | :--- |
| **Salud y Bienestar** | Esperanza de vida al nacer | `SP.DYN.LE00.IN` | Años |
| **Salud y Bienestar** | Mortalidad infantil | `SP.DYN.IMRT.IN` | Por cada 1,000 nacidos vivos |
| **Medio Ambiente** | Superficie forestal | `AG.LND.FRST.ZS` | % del área terrestre |
| **Medio Ambiente** | Emisiones de CO2 per cápita | `EN.ATM.CO2E.PC` | Toneladas métricas per cápita |
| **Demografía** | Población rural | `SP.RUR.TOTL.ZS` | % de la población total |
| **Demografía** | Crecimiento y población total | `SP.POP.GROW`, `SP.POP.TOTL` | % anual, personas |
""")
