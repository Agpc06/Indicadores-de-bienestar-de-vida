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
        fig_obj = px.scatter(
            df_pivot,
            x=ind_co2,
            y=ind_vida,
            color="Nombre Pais",
            trendline="ols",
            hover_name="Año",
            template="plotly_dark",
            labels={ind_co2: "Emisiones de CO2 (ton. per cápita)", ind_vida: "Esperanza de VIda (años)"}
        )
        st.plotly_chart(fig_obj, use_container_width=True)

    else:
        st.warning("No hay suficientes datos cruzados para visualizar la relación.")
