import streamlit as st 

st.set_page_config(
    page_title = "Objetivos",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

st.title("📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica")
st.markdown('---')

st.subheader('Objetivo general')
st.markdown('Analizar el impacto del desarrollo urbano sobre la esperanza de vida y la sostenibilidad ambiental en Latinoamérica desde 1963 hasta 2023')

st.markdown('---')
st.subheader('Objetivos Especificos')
st.markdown('''
- Caracterizar la evolución histórica de la mortalidad infantil y la esperanza de vida, en contraste con la cobertura forestal de la región
- Analizar el impacto de la variación poblacional sobre la conservación de los ecosistemas forestales, tomando en cuenta el porcentaje de dicha población que reside en zonas rurales de la región
- Evaluar el impacto de las emisiones de CO2 sobre la esperanza de vida al nacer en los paises de la región
''')