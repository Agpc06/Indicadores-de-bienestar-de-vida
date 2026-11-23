import os
from pathlib import Path
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno desde el archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent 
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def _obtener_credenciales():
    """Obtiene URL y KEY de Supabase desde .env o st.secrets."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    # Fallback para Streamlit Community Cloud (st.secrets)
    if not url or not key:
        try:
            if hasattr(st, "secrets"):
                url = url or st.secrets.get('SUPABASE_URL')
                key = key or st.secrets.get('SUPABASE_KEY')
        except Exception:
            pass
            
    return url, key

SUPABASE_URL, SUPABASE_KEY = _obtener_credenciales()

def get_supabase_client() -> Client:
    """Inicializa y devuelve el cliente de Supabase si las credenciales existen."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error al inicializar cliente de Supabase: {e}")
        return None

# Instancia global de supabase para retrocompatibilidad
supabase: Client = get_supabase_client()

def rescatar_nulos(df_nuevo, chunksize=1000):
    """
    Compara un DataFrame con la tabla indicators de Supabase y rellena los valores 
    que actualmente son NULL en la base de datos.
    """
    cliente = get_supabase_client()
    if not cliente:
        print("Cliente de Supabase no disponible.")
        return

    filas = len(df_nuevo)
    actualizados = 0
    
    for start in range(0, filas, chunksize):
        end = min(start + chunksize, filas)
        chunk = df_nuevo.iloc[start:end]

        for _, row in chunk.iterrows():
            try:
                res = cliente.table("indicators") \
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
                print(f"Error en fila {row['country_code']}-{row['year']}: {e}")
        time.sleep(1)
    print(f"Se han actualizado {actualizados} registros.")


def ejecutar_query(query_input): 
    """
    Envia un Query SQL a Supabase mediante la función RPC 'ejecutar_sql_crudo'
    y devuelve el resultado como un DataFrame de Pandas.
    """
    df_resultados = pd.DataFrame()
    cliente = get_supabase_client()
    
    if not cliente:
        st.error("No se pudo conectar a Supabase: credenciales no configuradas.")
        return df_resultados

    try:
        response = cliente.rpc('ejecutar_sql_crudo', {'query': query_input}).execute()
        datos_json = response.data
        
        if datos_json:
            df_resultados = pd.DataFrame(datos_json)
            st.dataframe(df_resultados, use_container_width=True)
        else:
            st.warning("La consulta se ejecutó, pero no devolvió ningún resultado.")
            
    except Exception as e:
        st.error(f"Error al ejecutar la consulta:\n{e}")
        
    return df_resultados


@st.cache_data(ttl=3600, show_spinner=False)
def obtener_datos(tabla: str) -> pd.DataFrame:
    """
    Obtiene los datos de una tabla específica en Supabase y los devuelve como DataFrame.
    Incluye paginación automática para evitar el límite de 1,000 filas de PostgREST
    y caché en Streamlit para optimizar el rendimiento.
    """
    cliente = get_supabase_client()
    if not cliente:
        st.warning("⚠️ No se han configurado las credenciales de Supabase (SUPABASE_URL y SUPABASE_KEY).")
        return pd.DataFrame()

    try:
        registros = []
        chunk_size = 1000
        offset = 0

        # Mapeo de nombre de tabla a consulta real
        tabla_real = 'investigación_denormalizada' if tabla == 'total' else tabla
        
        if tabla not in ['country', 'indicators', 'series', 'total']:
            st.error(f"Tabla solicitada no válida: '{tabla}'")
            return pd.DataFrame()

        # Paginación para traer todos los registros completos
        while True:
            response = cliente.schema('public').table(tabla_real) \
                .select('*') \
                .range(offset, offset + chunk_size - 1) \
                .execute()
                
            data = response.data
            if not data:
                break
                
            registros.extend(data)
            if len(data) < chunk_size:
                break
            offset += chunk_size

        if not registros:
            return pd.DataFrame()

        df = pd.DataFrame(registros)

        # Renombrado seguro por coincidencia de columnas existentes
        mapeo_columnas = {
            'country': {
                'country_code': 'Codigo Pais',
                'short_name': 'Nombre',
                'long_name': 'Nombre largo',
                'currency_unit': 'Moneda',
                'income_group': 'Nivel de Ingreso'
            },
            'indicators': {
                'country_code': 'Codigo Pais',
                'indicator_code': 'Codigo Indicador',
                'year': 'Año',
                'value': 'Valor'
            },
            'series': {
                'indicator_code': 'Codigo Indicador',
                'indicator_name': 'Nombre del Indicador',
                'topic': 'Tema',
                'definition': 'Definición',
                'unit_of_measure': 'Unidad de Medida'
            }
        }

        if tabla in mapeo_columnas:
            df = df.rename(columns=mapeo_columnas[tabla])

        return df

    except Exception as e:
        st.error(f"Error al obtener datos de la tabla '{tabla}': {e}")
        return pd.DataFrame()
