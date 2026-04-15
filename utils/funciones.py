import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path
import time
import pandas as pd
import streamlit as st

#Cargar variables de entorno desde el archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent 
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

#Obtener variables de entorno
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
#Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Creamos funcion para rellenar valores nulos segun datos de nuevos dataframes
def rescatar_nulos(df_nuevo, chunksize=1000):
    """
    Compara un DataFrame con una tabla de Supabase en intervalos de {chunksize} y rellena SOLO los valores 
    que actualmente son NULL en la base de datos.
    """
    filas = len(df_nuevo)
    actualizados = 0
    
    for start in range(0, filas, chunksize):
        end = min(start + chunksize, filas)
        chunk = df_nuevo.iloc[start:end]

        for _, row in chunk.iterrows():
            try:
                # Intentamos la actualización solo si el valor es NULL
                res = supabase.table("indicators") \
                    .update({"value": row['value']}) \
                    .match({
                        "country_code": row['country_code'],
                        "indicator_code": row['indicator_code'],
                        "year": row['year']
                    }) \
                    .filter("value", "is", "null") \
                    .execute()
                
                if res.data:
                    actualizados += len(res.data)
                    
            except Exception as e:
                    print(f" Error en fila {row['country_code']}-{row['year']}: {e}")
        # descanso de 2 segundos para evitar sobrecargar la base de datos
        time.sleep(2)
    print(f"Se han actualizado {actualizados} registros.")


def ejecutar_query(query_input): 
    """
    Envia un Query SQL en formato TEXT a Supabase, Supabase lo transforma y ejecuta el query, devuelve el resultado en formato JSON,
    Pandas transforma este formato a un dataframe y muestra el resultado
    """
    try:
        # Llamamos a una función creada en Supabase y le pasamos el texto
        response = supabase.rpc('ejecutar_sql_crudo', {'query': query_input}).execute()
        
        datos_json = response.data
        
        if datos_json:
            # Convertimos el dicccionario (json) en un dataframe
            df_resultados = pd.DataFrame(datos_json)
            st.dataframe(df_resultados, use_container_width=True)
        else:
            st.warning("La consulta se ejecutó, pero no devolvió ningún resultado")
            
    except Exception as e:
        st.error(f"Error en la consulta:\n{e}")
    return df_resultados

def obtener_datos(tabla):
    """
    Función para obtener datos de una tabla específica en Supabase y devolverlos 
    como un DataFrame de Pandas.
    """
    try:
        if tabla in ['country', 'indicators', 'series']:
            response = supabase.schema('public').table(tabla).select('*').execute()
            if response.data:
                df = pd.DataFrame(response.data)
                # Renombramos columnas según la tabla para mayor claridad
                if tabla == 'country':
                    df.columns = ['Codigo Pais', 'Nombre', 'Nombre largo', 'Moneda', 'Nivel de Ingreso']
                elif tabla == 'indicators':
                    df.columns = ['Codigo Pais', 'Codigo Indicador', 'Año', 'Valor']
                elif tabla == 'series':
                    df.columns = ['Codigo Indicador', 'Nombre del Indicador', 'Tema', 'Definición', 'Unidad de Medida']
                return df
            else:
                return pd.DataFrame()
        elif tabla == 'total':
            response = supabase.schema('public').table('investigación_denormalizada').select('*').execute()
            if response.data:
                df = pd.DataFrame(response.data)
                df.columns = ['Codigo Pais', 'Nombre Pais', 'Nivel de Ingreso', 'Codigo Indicador', 'Nombre Indicador', 'Año', 'Valor'] 
                return df
            else:
                return pd.DataFrame()
        else:
            print('Por favor solicitar una tabla válida')

    except Exception as e:
        print(f"Error al obtener datos de la tabla {tabla}: {e}")
        return pd.DataFrame()
    