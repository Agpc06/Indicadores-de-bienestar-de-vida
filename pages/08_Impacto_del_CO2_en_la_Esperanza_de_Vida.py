import streamlit as st
import pandas as pd
import plotly.express as px
from utils.funciones import supabase, obtener_datos_directo

df_impacto = obtener_datos_directo('total')

if not df_impacto.empty:

    ind_co2 = "CO2 emissions (metric tons per capita)"
    ind_vida = "Life expectancy at birth, total (years)"

    # Filtrado
    df_filtrado_obj = df_impacto[df_impacto['Nombre Indicador'].isin([ind_co2, ind_vida])]
    df_pivot = df_filtrado_obj.pivot_table(
        index=['Nombre Pais', 'Año'],
        columns='Nombre Indicador',
        values='Valor'
    ).dropna().reset_index()

    if not df_pivot.empty:
        # Filtros en Sidebar
        # --- 2. CONFIGURACIÓN DE FILTROS EN SIDEBAR ---
        st.sidebar.header("Filtros")

        # Creamos la lista de opciones: "Promedio Regional" + los países individuales
        paises_en_pivot = sorted(df_pivot["Nombre Pais"].unique())
        opciones_filtro = ["Promedio Regional"] + paises_en_pivot

        seleccion = st.sidebar.selectbox(
            "Seleccionar ámbito del análisis:",
            options=opciones_filtro,
            index=0  # Por defecto "Promedio Regional"
        )

        anios_en_pivot = sorted(df_pivot["Año"].unique())
        rango_anios_grafico = st.sidebar.slider(
            "Rango de Años:",
            min_value=int(min(anios_en_pivot)),
            max_value=int(max(anios_en_pivot)),
            value=(int(min(anios_en_pivot)), int(max(anios_en_pivot)))
        )

        # --- 3. LÓGICA DE FILTRADO DINÁMICO ---
        if seleccion == "Promedio Regional":
            # Si elige promedio, usamos el DataFrame agrupado que creamos antes
            df_filtrado_final = df_pivot.groupby('Año').mean(numeric_only=True).reset_index()
            df_filtrado_final["Nombre Pais"] = "Promedio Regional"  # Etiqueta para el color
        else:
            # Si elige un país, filtramos normalmente
            df_filtrado_final = df_pivot[
                (df_pivot["Nombre Pais"] == seleccion) &
                (df_pivot["Año"].between(rango_anios_grafico[0], rango_anios_grafico[1]))
                ]

        # --- 4. RENDERIZADO DE GRÁFICOS (Misma estructura de columnas) ---
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.subheader("Tendencias Históricas")
            st.write("*Evolución Temporal: CO2 vs Esperanza de Vida*")

            # Este gráfico siempre muestra el promedio para dar contexto regional
            df_promedio_regional = df_pivot.groupby('Año').mean(numeric_only=True).reset_index()
            fig_lineas = px.line(
                df_promedio_regional,
                x='Año',
                y=[ind_co2, ind_vida],
                markers=True,
                template="plotly_dark",
                color_discrete_map={ind_co2: "#FF073A", ind_vida: "#FFFFFF"}
            )
            fig_lineas.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis_title="Valores"
            )
            st.plotly_chart(fig_lineas, use_container_width=True)

        with col_graf2:
            st.subheader("Relación de Impacto")
            st.write(f"*Análisis de {seleccion}*")

            if not df_filtrado_final.empty:
                fig_scatter = px.scatter(
                    df_filtrado_final,
                    x=ind_co2,
                    y=ind_vida,
                    color="Nombre Pais" if seleccion == "Promedio Regional" else "Año",
                    trendline="ols",
                    template="plotly_dark",
                    color_continuous_scale="Viridis",
                    labels={ind_co2: "CO2", ind_vida: "Vida (Años)"}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.warning("No hay datos para los filtros seleccionados.")

        # Conclusión
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-top: 20px;">
            <h4 style="color: #3b82f6; margin-top:0;">Conclusión:</h4>
            <ul style="color: white;">
                <li><b>*Esperanza de vida*:</b> Presenta un crecimiento sostenido y estable, reflejando mejoras en sistemas de salud y calidad de vida regional.</li>
                <li><b>*Emisiones de CO2*:</b> Aunque muestran una tendencia al alza, presentan mayor volatilidad, vinculada directamente a los ciclos de industrialización y cambios en las matrices energéticas de los países latinos.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No hay suficientes datos cruzados para mostrar la correlación.")
else:
    st.error("No se detectaron las columnas necesarias en el CSV o la base de datos.")
