import pandas as pd
from sqlalchemy import create_engine, inspect
from utils.funciones import supabase

# Creamos un engine con database .sqlite
engine = create_engine('sqlite:///BD_preguntas.sqlite') 

inspector = inspect(engine)
tablas_existentes = inspector.get_table_names()

# Establecemos orden de subida para evitar errores de foreign keys
prioridad = ['country', 'series', 'indicators', 'footnotes', 'series_notes']
tablas_a_procesar = [t for t in prioridad if t in tablas_existentes]
tablas_a_procesar += [t for t in tablas_existentes if t not in prioridad]

for tabla in tablas_a_procesar:
    # Subimos rows en chunks de 1000 
    for chunk in pd.read_sql(f"SELECT * FROM {tabla}", con=engine, chunksize=1000):
        chunk = chunk.replace({float('nan'): None})
        # Convertimos valores NaN a None para que Postgres los entienda
        chunk = chunk.where(pd.notnull(chunk), None)

        registros = chunk.to_dict(orient='records')
        try:
            supabase.schema('original').table(tabla).insert(registros).execute()
        except Exception as e:
            print(f"Error en {tabla}: {e}") 
print("Database subida exitosamente")