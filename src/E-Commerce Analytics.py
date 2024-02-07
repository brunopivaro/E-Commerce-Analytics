import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(r"C:/Users/bruno/Downloads/E-Commerce Analytics/dados/dataset.csv")

# Verificando presença de valores nulos
print(df.isna().sum())

# Verificando se há valores duplicados
print(df.duplicated().sum())

# Verificando outliers
print(df.desconto.mean())
print(df.desconto.std())
print(df.desconto.hist())

sup = df.desconto.mean() + 3 * df.desconto.std()
inf = df.desconto.mean() - 3 * df.desconto.std()

df_desconto_outliers = df[(df.desconto <= inf) | (df.desconto >= sup)]
print(df_desconto_outliers.head())

df = df[(df.desconto > inf) & (df.desconto < sup)]

# Verificando se outras colunas numéricas possuem outliers
registro = np.array([True] * len(df))

# Colunas numéricas (exceto a de descontos)
num = ['numero_chamadas_cliente', 'avaliacao_cliente', 'compras_anteriores', 'custo_produto', 'peso_gramas']

for col in num:
    zscore = abs(stats.zscore(df[col]))
    registro = (zscore < 3) & registro

df = df[registro]