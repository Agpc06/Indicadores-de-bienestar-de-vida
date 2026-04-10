import pandas as pd 
from utils.funciones import rescatar_nulos, supabase

# URL de la pagina Our World in Data, que usaremos para buscar los valores faltantes
# Del indicador "CO2 per capita", obtenidos de un archivo .csv en esta misma pagina
url_owid = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
df_owid = pd.read_csv(url_owid)

# Seleccionamos columnas y eliminamos nulos del origen
df_owid = df_owid[['iso_code', 'year', 'co2_per_capita']].dropna()
df_owid = df_owid[(df_owid['year'] >= 1963) & (df_owid['year'] <= 2023)]
df_owid['indicator_code'] = 'EN.ATM.CO2E.PC'
df_owid.columns = ['country_code', 'year', 'value', 'indicator_code']
    
# Reordenamos columnas 
df_owid = df_owid[['country_code', 'indicator_code', 'year', 'value']]

# Ejecutamos funcion de rescate
rescatar_nulos(df_owid)