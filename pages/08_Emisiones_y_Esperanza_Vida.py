import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.funciones import obtener_datos

st.set_page_config(
    page_title='Emisiones CO2 y Esperanza de Vida',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

st.subheader('Objetivo 3: Evaluar el impacto de las emisiones de dióxido de carbono sobre la esperanza de vida al nacer en los países de la región')
st.markdown("""
Este objetivo examina la relación entre la huella de carbono derivada de la actividad industrial y urbana y la longevidad de la población.
A través de este análisis se explora si el progreso tecnológico e industrial ha tenido un efecto sostenido en la salud pública o si el incremento de emisiones plantea un límite ambiental y de salud (enmarcado en la hipótesis de la Curva de Kuznets Ambiental).
""")
st.markdown('---')

# Extraemos datos de Supabase
tabla = 'total'
with st.spinner('Obteniendo datos de Supabase...'):
    df = obtener_datos(tabla)

if df.empty:
    st.warning("No se pudieron cargar los datos de Supabase. Verifique las credenciales de conexión.")
    st.stop()

# Nombres y códigos de indicadores
cod_esp = 'SP.DYN.LE00.IN'
cod_co2 = 'EN.ATM.CO2E.PC'

# Filtrado flexible por nombre o código
df_esp = df[(df['indicator_code'] == cod_esp) | (df['indicator_name'].str.contains('Life expectancy', case=False, na=False))][['country_name', 'year', 'value']]
df_esp = df_esp.rename(columns={'value': 'esperanza_vida'}).dropna()

df_co2 = df[(df['indicator_code'] == cod_co2) | (df['indicator_name'].str.contains('CO2', case=False, na=False))][['country_name', 'year', 'value']]
df_co2 = df_co2.rename(columns={'value': 'emisiones_co2'}).dropna()

# Unir ambos indicadores
df_final = pd.merge(df_esp, df_co2, on=['country_name', 'year'], how='inner')

if df_final.empty:
    st.info("No se encontraron registros coincidentes para Esperanza de Vida y Emisiones de CO2.")
    st.stop()

# Filtro en la barra lateral
st.sidebar.subheader("Filtros")
lista_paises = ['Promedio Regional'] + sorted(df_final['country_name'].unique().tolist())
pais_sel = st.sidebar.selectbox("Seleccionar País (Objetivo 3):", lista_paises)

if pais_sel == 'Promedio Regional':
    data_plot = df_final.groupby('year').mean(numeric_only=True).reset_index()
    titulo = "Promedio Regional"
else:
    data_plot = df_final[df_final['country_name'] == pais_sel].sort_values(by='year')
    titulo = pais_sel

col1, col2 = st.columns(2)

# Gráfico 1: Evolución Temporal Comparativa (Doble Eje)
with col1:
    st.subheader("Evolución Temporal Comparativa")
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        x=data_plot['year'], y=data_plot['esperanza_vida'],
        mode='lines+markers', name='Esperanza de Vida (años)',
        line=dict(color='#27ae60', width=2.5)
    ))

    fig_line.add_trace(go.Scatter(
        x=data_plot['year'], y=data_plot['emisiones_co2'],
        mode='lines+markers', name='CO2 per cápita (ton)',
        line=dict(color='#e67e22', width=2.5), yaxis='y2'
    ))

    fig_line.update_layout(
        title=f"Esperanza de Vida vs. Emisiones de CO2 ({titulo})",
        yaxis=dict(
            title=dict(text="Años de Vida", font=dict(color="#27ae60"))
        ),
        yaxis2=dict(
            title=dict(text="CO2 (Toneladas per cápita)", font=dict(color="#e67e22")),
            overlaying='y',
            side='right'
        ),
        hovermode="x unified",
        template="plotly_white",
        height=380
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Gráfico 2: Diagrama de Dispersión / Curva de Relación
with col2:
    st.subheader("Relación: Emisiones CO2 vs. Esperanza de Vida")
    
    # Verificamos si statsmodels está disponible para trendline sin generar error
    trendline_option = None
    try:
        import statsmodels.api as _sm
        trendline_option = "ols"
    except ImportError:
        pass

    scatter_kwargs = {
        'x': 'emisiones_co2',
        'y': 'esperanza_vida',
        'color': 'year',
        'title': f"Trayectoria Histórica ({titulo})",
        'labels': {
            'emisiones_co2': 'Emisiones CO2 per cápita (ton)',
            'esperanza_vida': 'Esperanza de Vida (años)',
            'year': 'Año'
        },
        'color_continuous_scale': 'Turbo'
    }
    if trendline_option:
        scatter_kwargs['trendline'] = trendline_option

    fig_scatter = px.scatter(data_plot, **scatter_kwargs)
    fig_scatter.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Conclusiones y Métricas Dinámicas
st.markdown('---')
st.subheader("Conclusiones del Análisis")

if not data_plot.empty:
    inicio = data_plot.iloc[0]
    fin = data_plot.iloc[-1]

    delta_esp = fin['esperanza_vida'] - inicio['esperanza_vida']
    delta_co2 = fin['emisiones_co2'] - inicio['emisiones_co2']

    st.info(f"""
    **Resumen para {titulo} ({int(inicio['year'])} - {int(fin['year'])}):**

    *   **Esperanza de Vida:** {'Aumentó' if delta_esp >= 0 else 'Disminuyó'} en **{abs(delta_esp):.1f} años** (de {inicio['esperanza_vida']:.1f} a {fin['esperanza_vida']:.1f} años).
    *   **Emisiones de CO2 per cápita:** {'Aumentaron' if delta_co2 >= 0 else 'Se redujeron'} en **{abs(delta_co2):.2f} toneladas métricas** (de {inicio['emisiones_co2']:.2f} a {fin['emisiones_co2']:.2f} ton).
    """)

    st.markdown(f"""
    El análisis de la relación entre emisiones de carbono y la longevidad en **{titulo}** refleja los efectos de la industrialización sobre el bienestar social:

    1. **Fase Inicial de Progreso:** Durante las primeras décadas de industrialización y urbanización, el aumento en la producción y el uso de energía permitió mejoras sanitarias, mayor infraestructura médica y un crecimiento notable en la esperanza de vida.
    2. **Fase de Desaceleración y Costo Ambiental:** En etapas más recientes, los incrementos adicionales en las emisiones de CO2 muestran rendimientos decrecientes en la ganancia de longevidad, a la vez que intensifican riesgos climáticos y enfermedades asociadas a la polución ambiental.
    3. **Enfoque de Sostenibilidad:** Para desacoplar el bienestar humano del deterioro ambiental, las políticas de desarrollo regional deben priorizar la transición hacia matrices energéticas limpias y movilidad urbana sostenible.
    """)
