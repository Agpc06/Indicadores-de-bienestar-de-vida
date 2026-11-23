import pandas as pd 
from utils.funciones import rescatar_nulos

def procesar_owid_co2():
    # URL de la página Our World in Data para valores de CO2 per cápita
    url_owid = "https://ourworldindata.org/grapher/co-emissions-per-capita.csv?v=1&csvType=full&useColumnShortNames=true"
    storage_options = {'User-Agent': 'Mozilla/5.0'}
    
    df_owid = pd.read_csv(url_owid, storage_options=storage_options)

    # Seleccionamos columnas y eliminamos nulos
    df_owid = df_owid[['iso_code', 'year', 'co2_per_capita']].dropna()
    df_owid = df_owid[(df_owid['year'] >= 1963) & (df_owid['year'] <= 2023)]
    
    # Estandarizamos nombres de columnas y agregamos código de indicador
    df_owid['indicator_code'] = 'EN.ATM.CO2E.PC'
    df_owid = df_owid.rename(columns={'iso_code': 'country_code', 'co2_per_capita': 'value'})
    df_owid = df_owid[['country_code', 'indicator_code', 'year', 'value']]
    
    # Ejecutamos función de rescate
    rescatar_nulos(df_owid)

if __name__ == '__main__':
    procesar_owid_co2()
