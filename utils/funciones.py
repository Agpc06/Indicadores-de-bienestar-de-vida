import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path


#Cargar variables de entorno desde el archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent 
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

#Obtener variables de entorno
database_url = os.getenv('SUPABASE_DATABASE_URL')

engine = create_engine(database_url)

#Creamos funcion para rellenar valores nulos segun datos de nuevos dataframes
def rescatar_nulos(df_nuevo, engine):
    """
    Compara un DataFrame con una tabla de Supabase y rellena SOLO los valores 
    que actualmente son NULL en la base de datos.
    """
    try:
        #Subir el DataFrame a una tabla temporal en Supabase
        temp_table_name = f"temp_indicators"
        df_nuevo.to_sql(temp_table_name, engine, if_exists='replace', index=False)

        #Definir la consulta SQL de actualización 
        query = text(f"""
            UPDATE indicators AS principal
            SET value = temporal.value
            FROM {temp_table_name} AS temporal
            WHERE principal.country_code = temporal.country_code
            AND principal.indicator_code = temporal.indicator_code
            AND principal.year = temporal.year
            AND principal.value IS NULL;
        """)

        #Ejecutar transacción
        with engine.begin() as conn:
            result = conn.execute(query)

        #Borrar la tabla temporal
        with engine.begin() as conn:
            conn.execute(text(f"DROP TABLE {temp_table_name};"))

        print(f"Se han actualizado {result.rowcount} valores nulos")

    except Exception as e:
        print(f"Error durante el proceso: {e}")

