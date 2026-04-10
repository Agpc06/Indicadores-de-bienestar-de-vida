import wbgapi as wb 
from utils.funciones import rescatar_nulos, supabase

# "wbgapi" es la API del Banco Mundial, de donde esta basada la database de Kaggle utilizada en el proyecto
# realizamos este script para verificar si a la data utilizada le faltan valores de la data original

# Obtenemos la lista de los códigos de todos los paises de la region 
paises_latam = wb.region.members('LCN') 

# Pedimos los datos usando la lista de países y los indicadores a utilizar
indicators = ['SP.POP.TOTL','SP.POP.GROW','EN.ATM.CO2E.PC','AG.LND.FRST.ZS','SP.URB.TOTL.IN.ZS','SP.RUR.TOTL.ZS','SP.DYN.IMRT.IN','SP.DYN.LE00.IN','SE.PRM.ENRR' ]
df_paises = wb.data.DataFrame(indicators, paises_latam, time=range(1963, 2023))

# Modificamos el formato al mismo utilizado en nuestra database
df_wbg = df_paises.stack().reset_index()
df_wbg.columns = ['country_code', 'indicator_code', 'year', 'value']

# Limpiamos el formato del año
df_wbg['year'] = df_wbg['year'].str.replace('YR', '').astype(int)

# Ejecutamos funcion de rescate 
rescatar_nulos(df_wbg)

