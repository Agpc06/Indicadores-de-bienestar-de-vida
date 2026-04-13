import pandas as pd
from utils.funciones import obtener_datos, rescatar_nulos, supabase

tabla = 'indicators'
df = obtener_datos(tabla)

# Colocamos a las columnas los nombres originales
df.columns = ['country_code', 'indicator_code', 'year', 'value']

# Nos aaseguramos de que esten ordenadas por año para que la interpolación funcione
df = df.sort_values(by=['country_code', 'indicator_code', 'year'])

# Aplicamos la interpolación agrupada por pais e indicador
df['value'] = df.groupby(['country_code', 'indicator_code'])['value'].transform(
        lambda x: x.interpolate(method='linear', limit_direction='both')
    )

# Ejecutamos función de rescate
rescatar_nulos(df)