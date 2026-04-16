import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.funciones import obtener_datos, supabase

st.set_page_config(
    page_title='Evolución Histórica',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

st.subheader('Objetivo 1: Caracterizar la evolución histórica de la mortalidad infantil y la esperanza de vida, en contraste con la cobertura forestal de la región')
st.markdown('Este objetivo se centra en trazar una línea temporal comparativa entre indicadores clave de salud pública, en este caso, la tasa de mortalidad infantil y la esperanza de vida, y el indicador ambiental de cobertura forestal porcentual. El propósito es visualizar cómo las transformacion ambienta, ya sea naturalmente o por intervención humana, a lo largo de las décadas, se han correlacionado con los cambios en la supervivencia de la población latinoamericana.')
st.markdown('---')
# Extraemos datos de Supabase
tabla = 'total'
with st.spinner('Obteniendo datos de Supabase...'):
    df = obtener_datos(tabla) 

esperanza = "Life expectancy at birth, total (years)"  
mortalidad = "Mortality rate, infant (per 1,000 live births)" 
forest = "Forest area (% of land area)" 

# Filtramos 3 dataframes distintos, uno por cada indicador
df_esp = df[df['indicator_name'] == esperanza][['country_name', 'year', 'value']]
df_esp = df_esp.rename(columns={'value': 'esperanza_vida'})

df_mort = df[df['indicator_name'] == mortalidad][['country_name', 'year', 'value']]
df_mort = df_mort.rename(columns={'value': 'mortalidad_infantil'})

df_forest = df[df['indicator_name'] == forest][['country_name', 'year', 'value']]
df_forest = df_forest.rename(columns={'value': 'area_forestal'})

# Unimos ambos indicadores, por separado, con area forestal 
df_esp_forest = pd.merge(df_esp, df_forest, on=['country_name', 'year'], how='inner')

df_mort_forest = pd.merge(df_mort, df_forest, on=['country_name', 'year'], how='inner')

# Filtro en la sidebar
st.sidebar.subheader("Filtros")
lista_paises = ['Promedio Regional'] + sorted(df_esp_forest['country_name'].unique())
pais_sel = st.sidebar.selectbox("Seleccionar País:", lista_paises)

# Función para filtrar por país o promedio
def preparar_df(df, pais):
    if pais == 'Promedio Regional':
        return df.groupby('year').mean(numeric_only=True).reset_index()
    else:
        return df[df['country_name'] == pais]

data_1 = preparar_df(df_esp_forest, pais_sel)
data_2 = preparar_df(df_mort_forest, pais_sel)

titulo = "Promedio Regional" if pais_sel == 'Promedio Regional' else pais_sel

col1, col2 = st.columns(2)

# Visualizacion de Esperanza de Vida vs Bosques 
with col1:
    st.subheader("Esperanza de Vida vs. Area Forestal")
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=data_1['year'], y=data_1['esperanza_vida'],
        mode='lines+markers', name='Esperanza de Vida',
        line=dict(color='#2ecc71', width=2.5)
    ))

    fig1.add_trace(go.Scatter(
        x=data_1['year'], y=data_1['area_forestal'],
        mode='lines+markers', name='Area Forestal (%)',
        line=dict(color='#3498db', width=2.5), yaxis='y2'
    ))

    fig1.update_layout(
        title=f"Tendencias en {titulo}",
        yaxis=dict(
            title=dict(text="Años de Vida", font=dict(color="#2ecc71"))
        ),
        yaxis2=dict(
            title=dict(text="Area (%)", font=dict(color="#3498db")),
            overlaying='y',
            side='right'
        ),
        hovermode="x unified",
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

# Visualizacion Mortalidad Infantil vs Bosques
with col2:
    st.subheader("Mortalidad Infantil vs. Area Forestal")
    fig2 = go.Figure()
    
    # Eje Izquierdo: Mortalidad
    fig2.add_trace(go.Scatter(
        x=data_2['year'], y=data_2['mortalidad_infantil'],
        mode='lines+markers', name='Mortalidad Infantil',
        line=dict(color='#e74c3c', width=2.5)
    ))
    # Eje Derecho: Bosque
    fig2.add_trace(go.Scatter(
        x=data_2['year'], y=data_2['area_forestal'],
        mode='lines+markers', name='Area Forestal (%)',
        line=dict(color='#3498db', width=2.5), yaxis='y2'
    ))
    
    fig2.update_layout(
        title=f"Tendencias en {titulo}",
        yaxis=dict(
            title=dict(text="Muertes / 1000 nacidos", font=dict(color="#e74c3c"))
        ),
        yaxis2=dict(
            title=dict(text="Area (%)", font=dict(color="#3498db")),
            overlaying='y',
            side='right'
        ),
        hovermode="x unified",
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig2, use_container_width=True)

# Analisis de resultados
st.markdown('---')
st.subheader("Conclusión del Análisis")

if not data_1.empty:
    # Tomamos datos del primer y último año disponible en el dataframe filtrado
    inicio = data_1.iloc[0]
    fin = data_1.iloc[-1]
    
    # Cálculos
    delta_esp = fin['esperanza_vida'] - inicio['esperanza_vida']
    delta_mort = data_2.iloc[-1]['mortalidad_infantil'] - data_2.iloc[0]['mortalidad_infantil']
    delta_bosque = fin['area_forestal'] - inicio['area_forestal']

    st.info(f"""
    **Resumen para {titulo} ({int(inicio['year'])} - {int(fin['year'])}):**
    
    *   **Salud:** La esperanza de vida aumentó **{delta_esp:+.1f} años**, mientras que la mortalidad infantil 
        {'disminuyó' if delta_mort < 0 else 'aumentó'} en **{abs(delta_mort):+.1f}** puntos.
    *   **Ambiente:** Paralelamente, la cobertura boscosa 
        {'se redujo' if delta_bosque < 0 else 'aumentó'} en **{abs(delta_bosque):.1f}%**.
        
    Esta comparación directa permite observar si el mejoramiento de los indicadores de salud ha conllevado un costo ambiental 
    en términos de pérdida de biodiversidad o recursos forestales.
    """)

st.markdown('El análisis comparativo entre los indicadores de esperanza de vida, mortalidad infantil y  el área forestal revela una relación inversa significativa en el periodo estudiado.')

st.markdown('Por un lado, los datos evidencian un éxito indiscutible en el bienestar humano: la esperanza de vida promedio regional se extendió en 7.5 años y la mortalidad infantil se redujo drásticamente en 25.1 puntos. Esto refleja el impacto positivo de la urbanización, la industrialización y el acceso a servicios médicos de la población.')

st.markdown('Sin embargo, este progreso social ha conllevado un alto costo ambiental. La cobertura forestal regional sufrió una disminución del 3% durante el mismo lapso. La visualización gráfica sugiere que la expansión de las ciudades y la infraestructura necesaria para sostener el crecimiento poblacional y la mejora en los índices de salud se ha realizado, en parte, a expensas de la pérdida de ecosistemas boscosos.')

st.markdown('Por lo tanto, podemos concluir que, aunque el modelo de desarrollo urbano en Latinoamérica ha sido altamente efectivo para garantizar la supervivencia y longevidad de sus habitantes, ha mostrado una falta de sostenibilidad ambiental, comprometiendo los recursos naturales a futuro. ')