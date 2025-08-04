import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_participantes = pd.read_csv('PARTICIPANTES_2024.csv', sep = ';', encoding = 'latin1')

# filtro para apenas no estado do Rio de Janeiro
df_participantes_rj = df_participantes.loc[df_participantes['SG_UF_PROVA'] == 'RJ']

# apagando as colunas de codigo de municipio e codigo do estado de onde foi aplicado a prova
df_participantes_rj.drop(columns = ['CO_MUNICIPIO_PROVA', 'CO_UF_PROVA'])

# criação de uma base de dados com os filtros aplicados
df_participantes_rj.to_csv('Dados participantes enem 2024 - RJ.csv', sep = ';', index = False)