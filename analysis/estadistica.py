import pandas as pd
from scipy import stats

def calcular_correlacion(df, var_x, var_y):
    # Quitamos los nulos de las columnas que se seleccionaron
    datos_limpios = df[[var_x, var_y]].dropna()

    x = datos_limpios[var_x]
    y = datos_limpios[var_y]

    # Realizamos el Test de Normalidad Shapiro-Wilk
    _, p_norm_x = stats.shapiro(x)
    _, p_norm_y = stats.shapiro(y)

    # Si el P-Valor es menor a 0.05, entonces los datos no son normales
    es_normal = p_norm_x > 0.05 and p_norm_y > 0.05



