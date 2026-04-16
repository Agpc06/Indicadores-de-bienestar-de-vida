import streamlit as st
import pandas as pd
import plotly.express as px
from utils.funciones import supabase
from utils.funciones import obtener_datos_directo

st.header('🌍Impacto de las emisiones de CO2 sobre la Esperanza de Vida al Nacer')
#st.write()

#st.subheader()

df_impacto = obtener_datos_directo('total')

if not df_impacto.empty:
    ind_co2 = "CO2 emissions (metric tons per capita)"
    ind_vida = "Life expectancy at birth, total (years)"

    df_filtrado_obj = df_impacto[df_impacto['Nombre Indicador'].isin([ind_co2, ind_vida])]

    df_pivot = df_filtrado_obj.pivot_table(
        index=['Nombre Pais', 'Año'],
        columns='Nombre Indicador',
        values='Valor'
    ).dropna().reset_index()

    if not df_pivot.empty:
        # Filtro de país
        st.sidebar.header("Filtros")
        paises_en_pivot = sorted(df_pivot["Nombre Pais"].unique())
        paises_sel_grafico = st.sidebar.multiselect(
            "Seleccionar países para el análisis:",
            options=paises_en_pivot,
            default=paises_en_pivot
        )

        # Filtro de año
        anios_en_pivot = sorted(df_pivot["Año"].unique())
        rango_anios_grafico = st.sidebar.slider(
            "Rango de Años:",
            min_value=int(min(anios_en_pivot)),
            max_value=int(max(anios_en_pivot)),
            value=(int(min(anios_en_pivot)), int(max(anios_en_pivot)))
        )

        # Aplicamos los filtros
        df_filtrado_final=df_pivot[
            (df_pivot["Nombre Pais"].isin(paises_sel_grafico)) &
            (df_pivot["Año"].between(rango_anios_grafico[0], rango_anios_grafico[1]))
        ]

        if not df_filtrado_final.empty:
            fig_obj = px.scatter(
                df_filtrado_final,
                x=ind_co2,
                y=ind_vida,
                color="Nombre Pais",
                trendline="ols",
                hover_name="Año",
                template="plotly_dark",
                labels={ind_co2:"Emisiones de CO2 (ton. per cápita)", ind_vida:"Esperanza de Vida (años)"}
            )

        st.plotly_chart(fig_obj, use_container_width=True)

    else:
        st.warning("No hay suficientes datos cruzados para visualizar la relación.")
