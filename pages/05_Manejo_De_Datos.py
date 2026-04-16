import streamlit as st

st.set_page_config(
    page_title='Manejo de Datos',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

st.title('📊 Análisis del Impacto Urbano en la Esperanza de Vida y la Sostenibilidad Ambiental de Latinoamérica')
st.markdown('---')

st.subheader('Manejo de Datos')
st.markdown('Esta investigación fue realizada utilizando una base de datos sobre Indicadores de Desarrollo Mundial del Banco Mundial, extraída de la página web Kaggle. Dicha base de datos, a su vez, está conformada por la gran mayoría de datos sobre los Indicadores de Desarrollo Mundial del Banco Mundial, obtenidos directamente de su API. ')

st.markdown('Debido a que la tabla principal de la base de datos original poseía alrededor de 25 millones de registros, se tomó la decisión de migrar a Supabase, optimizando así las consultas SQL y el trabajo en equipo, ya que esto garantiza que todo el equipo trabaje sobre una misma base de datos, entre otras cosas.')

st.markdown('Luego de migrar a Supabase, se corrigieron discordancias entre valores de ciertas columnas y se segmentó la data, dejando solamente los datos útiles para nuestra investigación: los indicadores “Superficie Forestal, Emisiones de CO2, Mortalidad Infantil, Esperanza  de Vida, Tasa de Escolaridad en Primaria, Crecimiento Poblacional, y Porcentaje de Población Rural y Urbana”, de los países  de América Latina dentro de los años 1963 y 2023.')

st.markdown('Al obtener la data segmentada, nos dimos cuenta de  que faltaba una gran cantidad de valores. La solución pensada para este problema era clara: buscar otras fuentes de datos en la web.')

st.markdown('Hicimos una conexión con la API del Banco Mundial, para verificar que no faltaba ningún valor del origen. Luego, se obtuvieron datos faltantes de escolaridad y emisiones de dióxido de carbono a través de una conexión con 2 tablas distintas de una misma página  web: Our World In Data. Dicha página web extrae sus datos de fuentes oficiales (Como FAO, UNESCO, entre otros).')

st.markdown('Luego de realizar las conexiones mencionadas anteriormente, y de una ardua labor investigativa, se llegó a la conclusión de aplicar un método de interpolación lineal para estimar los pocos valores faltantes que quedaban, obteniendo así nuestra de datos final a utilizar en la investigación')