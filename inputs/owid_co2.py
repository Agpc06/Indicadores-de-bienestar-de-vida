import pandas as pd 
from utils.funciones import rescatar_nulos, supabase

# URL de la pagina Our World in Data, que usaremos para buscar los valores faltantes
# Del indicador "CO2 per capita", obtenidos de un archivo .csv en esta misma pagina
url_owid = "https://ourworldindata.org/grapher/co-emissions-per-capita.csv?v=1&csvType=full&useColumnShortNames=true"

# Agregamos el User-Agent para que el servidor nos autorice el paso
storage_options = {'User-Agent': 'Mozilla/5.0'}
df_owid = pd.read_csv(url_owid, storage_options=storage_options)

# Seleccionamos columnas y eliminamos nulos del origen
df_owid = df_owid[['iso_code', 'year', 'co2_per_capita']].dropna()
df_owid = df_owid[(df_owid['year'] >= 1963) & (df_owid['year'] <= 2023)]
df_owid['indicator_code'] = 'EN.ATM.CO2E.PC'
df_owid.columns = ['country_code', 'year', 'value', 'indicator_code']
    
# Reordenamos columnas 
df_owid = df_owid[['country_code', 'indicator_code', 'year', 'value']]

# Ejecutamos funcion de rescate
rescatar_nulos(df_owid)