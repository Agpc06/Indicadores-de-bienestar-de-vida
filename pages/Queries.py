import pandas as pd 
import streamlit as st 
from utils.funciones import ejecutar_query, supabase 

st.set_page_config(
    page_title="Consultas SQL",
    layout="wide"
)

st.title("Queries SQL")
st.markdown("---")

# Selector de queries predefinidos
query_seleccionado = st.selectbox(
        "**Selecciona una consulta:**",
        [
            "Query 1: Países con Desempeño Sostenido por Encima del Promedio Regional",
            "Query 2: Ranking de Indicadores con Mayor Brecha entre Grupos de Ingreso", 
            "Query 3: Evolución Interanual y Detección de Regresiones Significativas",
            "Query 4: Indicadores Huérfanos con Notas pero sin Datos Recientes",
            "Query 5: Países con Crecimiento Compuesto Sostenido y Ranking Global"
        ]
    )

if query_seleccionado == "Query 2: Ranking de Indicadores con Mayor Brecha entre Grupos de Ingreso": 
    st.subheader("**Ranking de Indicadores con Mayor Brecha entre Grupos de Ingreso**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
        Para cada categoría temática de indicadores, determina cuál es el indicador que presenta
        la mayor brecha porcentual entre el grupo de países de ingreso alto y el grupo de países
        de ingreso bajo, usando el promedio del año más reciente disponible para cada grupo.
        Incluye solo aquellos indicadores que tengan datos registrados para ambos grupos de
        ingreso en ese año, y muestra el nombre del indicador, el tema, el valor promedio de
        cada grupo y la brecha porcentual calculada.
""")
    with st.expander("**Ver Query**"):
        query_real = "SELECT * FROM query_2" 
        # query_2 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
        query = """
WITH PaisesObjetivos AS (
    -- Seleccionamos solo paises de ingreso alto y bajo
    SELECT country_code, income_group
    FROM original.country
    WHERE income_group IN ('High income', 'Low income')
),
DbFiltrada AS (
    SELECT 
        i.indicator_code, 
        i.year, 
        t.income_group, 
        i.value
    FROM original.indicators i
    JOIN PaisesObjetivos t ON i.country_code = t.country_code
),

UltimoAño AS (
    -- Año mas reciente para cada indicador
    SELECT indicator_code, MAX(year) AS max_year
    FROM DbFiltrada
    GROUP BY indicator_code
),

DataReciente AS (
    -- Filtramos por el año más reciente y aseguramos que existan ambos grupos de ingreso
    SELECT 
        f.indicator_code,
        f.income_group,
        f.value
    FROM DbFiltrada f
    JOIN UltimoAño u ON f.indicator_code = u.indicator_code AND f.year = u.max_year
    WHERE f.indicator_code IN (
        SELECT indicator_code 
        FROM DbFiltrada
        WHERE (indicator_code, year) IN (SELECT indicator_code, max_year FROM UltimoAño)
        GROUP BY indicator_code 
        HAVING COUNT(DISTINCT income_group) = 2
    )
),

Promedios AS (
    SELECT 
        indicator_code,
        AVG(CASE WHEN income_group = 'High income' THEN value END) AS avg_high,
        AVG(CASE WHEN income_group = 'Low income' THEN value END) AS avg_low
    FROM DataReciente
    GROUP BY indicator_code
    HAVING AVG(CASE WHEN income_group = 'High income' THEN value END) IS NOT NULL 
       AND AVG(CASE WHEN income_group = 'Low income' THEN value END) IS NOT NULL 
       AND AVG(CASE WHEN income_group = 'Low income' THEN value END) <> 0
),

Brecha AS (
    SELECT 
        indicator_code,
        avg_high,
        avg_low,
        ROUND((((avg_high - avg_low) / NULLIF(avg_low, 0)) * 100)::numeric, 2) AS pct_gap
    FROM Promedios
),

Ranking AS (
    SELECT 
        s.indicator_name,
        s.topic,
        b.avg_high,
        b.avg_low,
        b.pct_gap,
        ROW_NUMBER() OVER(PARTITION BY s.topic ORDER BY ABS(b.pct_gap) DESC) as rank
    FROM Brecha b
    JOIN original.series s ON b.indicator_code = s.indicator_code
)

-- RESULTADO FINAL
SELECT 
    topic AS "Tema",
    indicator_name AS "Nombre del Indicador",
    ROUND(avg_high::numeric, 2) AS "Promedio Ingreso Alto",
    ROUND(avg_low::numeric, 2) AS "Promedio Ingreso Bajo",
    pct_gap AS "Brecha Porcentual (%)"
FROM Ranking
WHERE rank = 1
ORDER BY pct_gap DESC     
        """  

        st.code(query, language ="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta a Supabase..."):
                try:
                    df = ejecutar_query(query_real)
                    if not df.empty:
                        st.success(f"Consulta ejecutada exitosamente.")
                    else: 
                        st.warning("No se encontraron datos")
                except Exception as e:
                    st.error(f"Error al ejecutar consulta: {str(e)}")