import pandas as pd
from utils.funciones import obtener_datos, rescatar_nulos

def ejecutar_interpolacion():
    tabla = 'indicators'
    df = obtener_datos(tabla)

    if df.empty:
        print("No se encontraron datos para realizar la interpolación.")
        return

    # Normalizamos nombres de columnas según idioma
    mapeo = {
        'Codigo Pais': 'country_code',
        'Codigo Indicador': 'indicator_code',
        'Año': 'year',
        'Valor': 'value'
    }
    df = df.rename(columns=mapeo)

    # Nos aseguramos de que existan las columnas requeridas
    cols_requeridas = ['country_code', 'indicator_code', 'year', 'value']
    if not all(col in df.columns for col in cols_requeridas):
        print(f"Columnas requeridas no encontradas. Columnas presentes: {df.columns.tolist()}")
        return

    # Nos aseguramos de que estén ordenadas por año para que la interpolación funcione
    df = df.sort_values(by=['country_code', 'indicator_code', 'year'])

    # Aplicamos la interpolación lineal agrupada por país e indicador
    df['value'] = df.groupby(['country_code', 'indicator_code'])['value'].transform(
        lambda x: x.interpolate(method='linear', limit_direction='both')
    )

    # Ejecutamos función de rescate para subir valores recuperados
    rescatar_nulos(df)

if __name__ == '__main__':
    ejecutar_interpolacion()
