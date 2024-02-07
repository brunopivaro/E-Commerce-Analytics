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

# Remove registros com z-score abaixo de 3 nas colunas numericas
df = df[registro]

# Criando um bkp do meu dataset
df_bkp = df.copy()

# Todo atraso nos envios dos produtos são iguais? A prioridade do envio do produto afeta no seu atraso?
# Se a prioridade for alta e tiver atraso, definiremos como 'CRÍTICO', caso tenha prioridade media, consideraremos 'PROBLEMÁTICO',
# se a prioridade for baixa, 'TOLERÁVEL', ademais o envio foi feito no prazo

df_bkp["performance_envio"] = np.nan

df_bkp["performance_envio"] = np.where(
    (df_bkp["prioridade_produto"] == 'alta') & (df_bkp["entregue_no_prazo"] == 0), "Atraso Crítico",
    np.where(
        (df_bkp["prioridade_produto"] == 'media') & (df_bkp["entregue_no_prazo"] == 0), "Atraso Problematico",
        np.where(
            (df_bkp["prioridade_produto"] == 'baixo') & (df_bkp["entregue_no_prazo"] == 0), "Atraso Toleravel", "Sem Atraso"
        )
    )
)

print(df_bkp["performance_envio"].value_counts())

# Agregação dos dados
df_report = df_bkp.groupby(['performance_envio', 'entregue_no_prazo']).agg({'prioridade_produto': ['count']}).reset_index()
df_report.columns = ['performance_envio', 'entregue_no_prazo', 'contagem']
print(df_report.head())

# Transformando linha em coluna e coluna em linha (CrossTable)
df_report = pd.pivot_table(
    df_report,
    index = 'performance_envio',
    columns = 'entregue_no_prazo',
    values = 'contagem'
).reset_index()

df_report.columns = ['Status Envio', 'Total Atraso', 'Total no Prazo']
print(df_report.head())

# Unificando as duas colunas
df_report['Total no Prazo'] = df_report['Total no Prazo'].replace(np.nan, 0)
df_report["Total"] = df_report['Total Atraso'] + df_report['Total no Prazo']
df_report.drop(df_report.columns[[1, 2]], axis = 1, inplace = True)

print(df_report.head())