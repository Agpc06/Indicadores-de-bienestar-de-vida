import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.funciones import obtener_datos, supabase 


st.set_page_config(
    page_title='Impacto Poblacional',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

st.subheader('Objetivo 2: Analizar el impacto de la variación poblacional sobre la conservación de los ecosistemas forestales, tomando en cuenta el porcentaje de dicha población que reside en zonas rurales de la región')
st.markdown('Aquí se examina la dinámica demográfica de la región, prestando especial atención a la transición de la población rural a urbana. Se busca cuantificar cómo los cambios en la densidad poblacional y el porcentaje de habitantes en zonas rurales han ejercido presión sobre la conservación de los ecosistemas forestales, identificando patrones de deforestación asociados al crecimiento poblacional.')

# Llamamos datos del supabase
forest = "Forest area (% of land area)"
rural = "Rural population (% of total population)"

tabla = 'total'
with st.spinner('Obteniendo datos de Supabase...'):
    df = obtener_datos(tabla)

# Filtramos 2 dataframes distintos
df_forest = df[df['indicator_name'] == forest][['country_name', 'year', 'value']]
df_forest = df_forest.rename(columns={'value': 'area_forestal'})

df_rural = df[df['indicator_name'] == rural][['country_name', 'year', 'value']]
df_rural = df_rural.rename(columns={'value': 'poblacion_rural'})

# Unimos Area Forestal con Población Rural
df_final = pd.merge(df_forest, df_rural, on=['country_name', 'year'], how='inner')


# Filtro en la sidebar
lista_paises = ['Promedio Regional'] + sorted(df_final['country_name'].unique())
pais_sel = st.sidebar.selectbox("Seleccionar País (Objetivo 2):", lista_paises)

if pais_sel == 'Promedio Regional':
    data_plot = df_final.groupby('year').mean(numeric_only=True).reset_index()
    titulo = "Promedio Regional"
else:
    data_plot = df_final[df_final['country_name'] == pais_sel]
    titulo = pais_sel

col1, col2 = st.columns(2)

# Grafico de lineas para evolución temporal
with col1:
    st.subheader("Tendencias Históricas")
    fig_evol = go.Figure()
    
    fig_evol.add_trace(go.Scatter(
        x=data_plot['year'], y=data_plot['poblacion_rural'],
        mode='lines+markers', name='Población Rural (%)',
        line=dict(color='#9b59b6', width=2.5) 
    ))
    
    fig_evol.add_trace(go.Scatter(
        x=data_plot['year'], y=data_plot['area_forestal'],
        mode='lines+markers', name='Area Forestal (%)',
        line=dict(color='#3498db', width=2.5), yaxis='y2'
    ))

    fig_evol.update_layout(
        title=f"Urbanización vs. Bosques ({titulo})",
        yaxis=dict(
            title=dict(text="Rural (%)", font=dict(color="#9b59b6"))
        ),
        yaxis2=dict(
            title=dict(text="Bosque (%)", font=dict(color="#3498db")),
            overlaying='y',
            side='right'
        ),
        hovermode="x unified",
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig_evol, use_container_width=True)

# Grafico de dispersión para análisis de impacto 
with col2:
    st.subheader("Relación de Impacto")
    
    fig_corr = px.scatter(
        data_plot,
        x='poblacion_rural',
        y='area_forestal',
        color='year',
        title="Correlación: Rural vs Bosque",
        labels={'poblacion_rural': 'Población Rural (%)', 'area_forestal': 'Area Forestal (%)'},
        color_continuous_scale='Viridis'
    )

    st.plotly_chart(fig_corr, use_container_width=True)

# Conclusiones
st.markdown('---')
st.subheader("Conclusión")

if not data_plot.empty:
    inicio_o = data_plot.iloc[0]
    fin_o = data_plot.iloc[-1]
    
    delta_rural = fin_o['poblacion_rural'] - inicio_o['poblacion_rural']
    delta_bosque_o = fin_o['area_forestal'] - inicio_o['area_forestal']
    
    st.info(f"""
    **Resumen Demográfico y Ambiental ({titulo}):**
    
    *   **Transición Urbana:** La población rural disminuyó en **{abs(delta_rural):.1f}%** (la gente se mudó a ciudades).
    *   **Impacto en Bosques:** Durante este éxodo rural, la cobertura boscosa 
        {'se recuperó' if delta_bosque_o > 0 else 'se redujo'} en **{abs(delta_bosque_o):.1f}%**.
        
    {'El gráfico de dispersión sugiere que la reducción de la presión directa de la población rural sobre la tierra NO ha detenido la deforestación, posiblemente debido a actividades industriales o agrícolas a gran escala.' 
    if delta_bosque_o < 0 
    else 'El gráfico sugiere que la urbanización podría haber aliviado la presión sobre los bosques, permitiendo una recuperación de la cobertura forestal.'}
    """)

    st.markdown(f'El análisis comparativo entre el cambio de la población rural y la cobertura forestal para **{titulo}** revela un patrón relevante sobre la dinámica demográfica y el medio ambiente.')

    st.markdown(f'Los datos muestran que, mientras la población rural presentó una variación de {delta_rural:+.1f}%, la cobertura forestal varió en {delta_bosque_o:+.1f}%. La visualización de dispersión permite evaluar el grado de correlación entre el cambio de la población rural y la superficie de áreas forestales.')

    st.markdown('Esto sugiere que la presión sobre los ecosistemas no necesariamente desaparece al haber menos personas en el campo, sino que se transforma. A medida que la población se concentró en ciudades, la demanda de tierras para la agroindustria, la infraestructura y la explotación de recursos para abastecer los centros urbanos se intensificó, incidiendo en la pérdida de áreas forestales independientemente de la densidad poblacional rural.')

    st.markdown('Por tanto, podemos concluir que la reducción de población en zonas rurales no frena automáticamente la deforestación y que las estrategias de conservación efectivas deben abordar procesos industriales y de consumo a gran escala.')
