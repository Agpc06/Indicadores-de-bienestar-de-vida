import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from utils.funciones import get_supabase_client

def cargar_base_sqlite_a_supabase(db_file='BD_preguntas.sqlite'):
    """
    Lee las tablas de una base de datos local SQLite y las sube
    al esquema 'original' de Supabase en bloques de 1,000 registros.
    """
    if not os.path.exists(db_file):
        print(f"⚠️ Archivo '{db_file}' no encontrado. Coloque el archivo SQLite en la raíz antes de ejecutar la carga.")
        return

    cliente = get_supabase_client()
    if not cliente:
        print("⚠️ No se pudo inicializar el cliente de Supabase. Verifique las credenciales.")
        return

    engine = create_engine(f'sqlite:///{db_file}') 
    inspector = inspect(engine)
    tablas_existentes = inspector.get_table_names()

    # Establecemos orden de subida para respetar llaves foráneas
    prioridad = ['country', 'series', 'indicators', 'footnotes', 'series_notes']
    tablas_a_procesar = [t for t in prioridad if t in tablas_existentes]
    tablas_a_procesar += [t for t in tablas_existentes if t not in prioridad]

    print(f"Tablas a procesar: {tablas_a_procesar}")

    for tabla in tablas_a_procesar:
        print(f"Cargando tabla: {tabla}...")
        for chunk in pd.read_sql(f"SELECT * FROM {tabla}", con=engine, chunksize=1000):
            chunk = chunk.replace({float('nan'): None})
            chunk = chunk.where(pd.notnull(chunk), None)
            registros = chunk.to_dict(orient='records')
            try:
                cliente.schema('original').table(tabla).insert(registros).execute()
            except Exception as e:
                print(f"Error en tabla {tabla}: {e}")

    print("Carga finalizada con éxito.")

if __name__ == '__main__':
    cargar_base_sqlite_a_supabase()
