import streamlit as st 
from utils.funciones import obtener_datos, supabase 

# Configurar la página
st.set_page_config(
    page_title="Indicadores de Desarrollo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

st.subheader('Datos')

tabla_seleccionada = st.selectbox(
    "Consulta una tabla:",
    ['country','indicators','series','total']
)

with st.spinner(f'Cargando tabla {tabla_seleccionada}'):
    df = obtener_datos(tabla_seleccionada)

if not df.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", len(df))
    
    with col2:
        st.metric("Total de Columnas", len(df.columns))

    if tabla_seleccionada in ['total', 'indicators']:
        with col3:
            st.metric("Rango de Tiempo", '1963-2023')
    elif tabla_seleccionada == 'country':
        with col3:
            st.metric('Region', 'América Latina y Centro América')
    else:
        pass
    
    st.markdown('---')
    st.dataframe(df.head(25))

    # Botón para descargar
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"{tabla_seleccionada}_data.csv",
        mime="text/csv"
    )

else:
    st.error(f"No se pudieron cargar los datos de la tabla '{tabla_seleccionada}'")

# Footer
st.markdown("---")
st.markdown("📊 **Análisis Exploratorio inicial** - Grupo 4 (Computación 2) - Universidad Central de Venezuela")