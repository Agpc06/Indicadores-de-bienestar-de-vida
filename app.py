import streamlit as st 
from utils.funciones import obtener_datos, SUPABASE_URL, SUPABASE_KEY

# Configurar la página
st.set_page_config(
    page_title="Indicadores de Desarrollo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("⚠️ **Aviso de Configuración:** No se han detectado las credenciales de Supabase (`SUPABASE_URL` y `SUPABASE_KEY`). Por favor configúralas en tu archivo `.env` o en `st.secrets` para habilitar las consultas a la base de datos.")

st.subheader('Explorador de Datos')

tabla_seleccionada = st.selectbox(
    "Selecciona una tabla para explorar:",
    ['country', 'indicators', 'series', 'total'],
    format_func=lambda x: {
        'country': 'Paises (country)',
        'indicators': 'Indicadores (indicators)',
        'series': 'Series y Definiciones (series)',
        'total': 'Dataset Consolidado (investigación_denormalizada)'
    }.get(x, x)
)

with st.spinner(f'Cargando tabla {tabla_seleccionada}...'):
    df = obtener_datos(tabla_seleccionada)

if not df.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    
    with col2:
        st.metric("Total de Columnas", len(df.columns))

    with col3:
        if 'Año' in df.columns:
            st.metric("Rango de Tiempo", f"{int(df['Año'].min())} - {int(df['Año'].max())}")
        elif 'year' in df.columns:
            st.metric("Rango de Tiempo", f"{int(df['year'].min())} - {int(df['year'].max())}")
        elif tabla_seleccionada == 'country':
            st.metric('Región Principal', 'América Latina y el Caribe')
        else:
            st.metric('Estado', 'Datos disponibles')
    
    st.markdown('---')
    st.markdown(f"**Vista previa (primeros 25 registros de {len(df):,}):**")
    st.dataframe(df.head(25), use_container_width=True)

    # Botón para descargar con codificación utf-8-sig (compatible con Excel)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar Datos Completos (CSV)",
        data=csv,
        file_name=f"{tabla_seleccionada}_data.csv",
        mime="text/csv"
    )

else:
    st.info(f"No se pudieron cargar datos para la tabla '{tabla_seleccionada}'. Verifique la conectividad con Supabase.")

# Footer
st.markdown("---")
st.markdown("📊 **Análisis Exploratorio inicial** - Grupo 4 (Computación 2) - Universidad Central de Venezuela")
