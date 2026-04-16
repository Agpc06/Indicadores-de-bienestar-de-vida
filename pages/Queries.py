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
if query_seleccionado == "Query 1: Países con Desempeño Sostenido por Encima del Promedio Regional": 
    st.subheader("**Países con Desempeño Sostenido por Encima del Promedio Regional**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
        Identifica todos los países que, durante los últimos 10 años con datos disponibles, hayan
        mantenido consistentemente su valor por encima del promedio de su región para un mismo
        indicador de desarrollo económico. Solo considera países que pertenezcan al grupo de
        ingresos medios o altos, y muestra el nombre del país, su región, el nombre del indicador,
        el promedio regional y el promedio del país en ese período. Ordena los resultados por la
        diferencia entre ambos promedios de forma descendente.
""")
    with st.expander("**Ver Query**"):
        query_real = "SELECT * FROM query_1" 
        # query_1 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
        query = """
WITH VentanaTiempo AS (
    -- Obtiene el año más reciente disponible
    SELECT MAX(year) AS año_maximo
    FROM original.indicators
),
DatosFiltrados AS (
    -- Selecciona datos directamente de indicators y une con country 
    SELECT
        c.short_name,
        i.country_code,
        c.region,
        s.indicator_name,
        i.indicator_code,
        i.Year,
        i.value
    FROM original.indicators i
    JOIN original.country c ON i.country_code = c.country_code
    JOIN original.series s ON i.indicator_code = s.indicator_code
    CROSS JOIN VentanaTiempo vt
    WHERE
        i.year >= vt.año_maximo - 9 AND i.year <= vt.año_maximo
        AND c.income_group IN ('High income', 'Upper middle income')
        AND c.region IS NOT NULL
        AND s.topic IN ('Financial Sector', 'Economic Policy & Debt')
        AND i.value IS NOT NULL
),
PromedioRegionAnual AS (
    -- Calcular el promedio de la región por año e indicador
    SELECT
        region,
        indicator_code,
        year,
        AVG(Value) AS valor_promedio_region
    FROM DatosFiltrados
    GROUP BY region, indicator_code, year
),
ComparacionAnual AS (
    -- Compara país vs región año a año
    SELECT
        df.country_code,
        df.short_name,
        df.region,
        df.indicator_code,
        df.indicator_name,
        df.year,
        df.value AS valor_pais,
        pra.valor_promedio_region,
        CASE WHEN df.Value > pra.valor_promedio_region THEN 1 ELSE 0 END AS supera_promedio
    FROM DatosFiltrados df
    JOIN PromedioRegionAnual pra
        ON df.region = pra.region
        AND df.indicator_code = pra.indicator_code
        AND df.year = pra.year
),
PaisesConsistentes AS (
    -- Filtra países que superaron el promedio en TODOS los años del periodo
    SELECT
        country_code,
        indicator_code
    FROM ComparacionAnual
    GROUP BY country_code, indicator_code
    HAVING SUM(supera_promedio) = COUNT(*)
),
PromediosTotales AS (
    -- Calcula los promedios del periodo 
    SELECT
        ca.short_name,
        ca.region,
        ca.indicator_name,
        AVG(ca.valor_pais) AS promedio_pais,
        AVG(ca.valor_promedio_region) AS promedio_region
    FROM ComparacionAnual ca
    JOIN PaisesConsistentes pc
        ON ca.country_code = pc.country_code
        AND ca.indicator_code = pc.indicator_code
    GROUP BY ca.short_name, ca.region, ca.indicator_name
)
-- Resultado final 
SELECT
    short_name AS nombre_pais,
    region AS region,
    indicator_name AS nombre_indicador,
    ROUND(promedio_region::numeric, 2) AS "Promedio Regional",
    ROUND(promedio_pais::numeric, 2) AS "Promedio País",
    ROUND((promedio_pais - promedio_region)::numeric, 2) AS Diferencia
FROM PromediosTotales
ORDER BY Diferencia DESC;  
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

#Query Lau
  
if query_seleccionado == "Query 4: Indicadores Huérfanos con Notas pero sin Datos Recientes": 
    st.subheader("**Indicadores Huérfanos con Notas pero sin Datos Recientes**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
        Encuentra todos los indicadores que cumplan simultáneamente las siguientes condiciones:
        1) Tienen al menos una nota de serie registrada posterior al año 2010.
        2) Tienen al menos una nota a nivel de país asociada.
        3) No tienen ningún valor de dato registrado en los últimos 5 años disponibles en la tabla
        de mediciones.
        Para cada indicador encontrado, muestra su código, nombre completo, tema, el año
        de la nota más reciente y la cantidad de países con notas asociadas.
""")
    with st.expander("**Ver Query**"):
        query_real = "SELECT * FROM query_4" 
        # query_4 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
        query = """
    WITH ConfiguracionTiempo AS (
    -- Obtiene el año más reciente de mediciones
    SELECT MAX(year) AS año_maximo
    FROM original.indicators
),
IndicadoresConNotasRecientes AS ( 
    -- Filtramos por año > 2010
    SELECT DISTINCT
        s.indicator_code,
        MAX(s.year) AS año_nota_mas_reciente
    FROM original.series_notes s
    WHERE s.year > 2010
    GROUP BY s.indicator_code
),
IndicadoresConNotaPais AS (
    -- Contamos países con notas 
    SELECT
        f.indicator_code,
        COUNT(DISTINCT f.country_code) AS cantidad_paises_con_notas
    FROM original.footnotes f
    GROUP BY f.indicator_code
),
IndicadoresSinDatosRecientes AS (
    -- Indicadores que SÍ tienen datos en los últimos 5 años
    SELECT DISTINCT
        i.indicator_code
    FROM original.indicators i
    CROSS JOIN ConfiguracionTiempo ct
    WHERE 
        i.value IS NOT NULL
        AND i.year >= (ct.año_maximo - 4)
)
-- Resultado Final
SELECT
    s.indicator_code AS codigo_indicador,
    s.indicator_name AS nombre_completo,
    s.topic AS tema,
    inr.año_nota_mas_reciente,
    icp.cantidad_paises_con_notas
FROM original.series s
JOIN IndicadoresConNotasRecientes inr
    ON s.indicator_code = inr.indicator_code
JOIN IndicadoresConNotaPais icp
    ON s.indicator_code = icp.indicator_code
WHERE NOT EXISTS (
    SELECT 1
    FROM IndicadoresSinDatosRecientes isdr
    WHERE isdr.indicator_code = s.indicator_code
)
ORDER BY inr.año_nota_mas_reciente DESC;
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
if query_seleccionado == "Query 5: Países con Crecimiento Compuesto Sostenido y Ranking Global": 
    st.subheader("**Evolución Interanual y Detección de Regresiones Significativas**")
 
    with st.expander("**Ver Pregunta**"):
        st.text("""
        Calcula la tasa de crecimiento anual compuesto (CAGR) de un indicador de ingreso
        nacional para todos los países que tengan datos tanto en el año 2000 como en el 2020.
        Luego, asigna a cada país un ranking global y un ranking dentro de su grupo de ingresos
        según esa tasa de crecimiento. Muestra únicamente los 5 países con mayor CAGR de
        cada grupo de ingresos, incluyendo el nombre del país, su grupo de ingresos, la región,
        el CAGR calculado, el ranking global y el ranking por grupo. El CAGR se define como:
        ((valor_final / valor_inicial) ^ (1/n) - 1) * 100, donde n = número de años.
""")
    with st.expander("**Ver Query**"):
        query_real = "SELECT * FROM query_3" 
        # query_3 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
        query = """
    WITH DatosFiltrados AS (
    SELECT
        c.short_name AS country_name,  
        s.indicator_name,             
        i.country_code,
        i.indicator_code,
        i.year,                        
        i.value                         
    FROM original.indicators i
    JOIN original.country c ON i.country_code = c.country_code
    JOIN original.series s ON i.indicator_code = s.indicator_code
    WHERE
        c.region = 'Latin America & Caribbean'
        AND s.topic IN ('Health', 'Education')
        AND i.year BETWEEN 2000 AND 2020
        AND i.value IS NOT NULL
        AND i.value <> 0
),
EvolucionAnual AS (
    SELECT
        country_name,
        indicator_name,
        year,
        value AS valor_actual,
        LAG(value) OVER (PARTITION BY country_code, indicator_code ORDER BY year) AS valor_anterior
    FROM DatosFiltrados
),
RegresionesDetectadas AS (
    SELECT
        country_name,
        indicator_name,
        year AS año_caida,
        valor_anterior,
        valor_actual,
        ((valor_actual - valor_anterior) / valor_anterior) * 100 AS variacion_porcentual
    FROM EvolucionAnual
    WHERE
        valor_anterior IS NOT NULL
        AND ((valor_actual - valor_anterior) / valor_anterior) * 100 < -20
)
-- Resultado final 
SELECT
    country_name AS nombre_pais,
    indicator_name AS nombre_indicador,
    año_caida,
    valor_anterior,
    valor_actual,
    ROUND(variacion_porcentual::numeric, 2) AS variacion_porcentual
FROM RegresionesDetectadas
ORDER BY variacion_porcentual ASC, nombre_pais ASC, año_caida ASC;
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