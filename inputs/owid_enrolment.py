import pandas as pd
from utils.funciones import rescatar_nulos

def procesar_owid_enrolment():
    # URL de Our World in Data para School Enrolment, Primary (% gross)
    url = 'https://ourworldindata.org/grapher/primary-secondary-enrollment-completion-rates.csv?v=1&csvType=full&useColumnShortNames=true'
    storage_options = {'User-Agent': 'Mozilla/5.0'}
    
    df_owid = pd.read_csv(url, storage_options=storage_options)

    # Seleccionamos columnas y eliminamos nulos
    df_owid = df_owid[['code', 'year', 'gross_enrolment_ratio__primary__both_sexes__pct']].dropna()
    df_owid = df_owid[(df_owid['year'] >= 1963) & (df_owid['year'] <= 2023)]
    
    # Estandarizamos columnas
    df_owid['indicator_code'] = 'SE.PRM.ENRR'
    df_owid = df_owid.rename(columns={
        'code': 'country_code',
        'gross_enrolment_ratio__primary__both_sexes__pct': 'value'
    })
    df_owid = df_owid[['country_code', 'indicator_code', 'year', 'value']]
        
    # Ejecutamos función de rescate
    rescatar_nulos(df_owid)

if __name__ == '__main__':
    procesar_owid_enrolment()
