import wbgapi as wb 
from utils.funciones import rescatar_nulos

def procesar_wbgapi():
    # Obtenemos la lista de los códigos de todos los países de la región 
    paises_latam = wb.region.members('LCN') 

    # Indicadores a consultar (rango 1963 a 2023 inclusive)
    indicators = ['SP.POP.TOTL','SP.POP.GROW','EN.ATM.CO2E.PC','AG.LND.FRST.ZS','SP.URB.TOTL.IN.ZS','SP.RUR.TOTL.ZS','SP.DYN.IMRT.IN','SP.DYN.LE00.IN','SE.PRM.ENRR']
    df_paises = wb.data.DataFrame(indicators, paises_latam, time=range(1963, 2024))

    # Modificamos el formato al mismo utilizado en nuestra base de datos
    df_wbg = df_paises.stack().reset_index()
    df_wbg.columns = ['country_code', 'indicator_code', 'year', 'value']

    # Limpiamos el formato del año
    df_wbg['year'] = df_wbg['year'].str.replace('YR', '').astype(int)

    # Ejecutamos función de rescate
    rescatar_nulos(df_wbg)

if __name__ == '__main__':
    procesar_wbgapi()


