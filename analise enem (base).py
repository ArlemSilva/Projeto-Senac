import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# TRATAMENTO
df_resultados = pd.read_csv('RESULTADOS_2024.csv', sep = ';', encoding = 'latin1')

# filtro para apenas no estado do Rio de Janeiro
df_resultados_rj = df_resultados.loc[df_resultados['SG_UF_ESC'] == 'RJ']

# eliminando as colunas dos gabaritos e respostas dos participantes
df_resultados_rj = df_resultados_rj.drop(columns = ['TX_RESPOSTAS_CN','TX_RESPOSTAS_CH','TX_RESPOSTAS_LC','TX_RESPOSTAS_MT','TX_GABARITO_CN','TX_GABARITO_CH','TX_GABARITO_LC','TX_GABARITO_MT'], axis = 1)

# eliminando as colunas dos codigos dos tipos de provas
df_resultados_rj = df_resultados_rj.drop(columns = ['CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC',], axis = 1)

# eliminando as colunas com os codigos do municipio da escola e codigo do estado da onde foi aplicado a prova
df_resultados_rj = df_resultados_rj.drop(columns = ['CO_MUNICIPIO_ESC', 'CO_UF_ESC'], axis = 1)

# Criando uma COLUNA com a nota media total do enem de cada inscrito
df_resultados_rj['NOTA_MEDIA'] = df_resultados_rj[['NU_NOTA_CN','NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis = 1)

# transformando o Data Frame tratado para csv (para utilizar no power bi e analisar com  graficos)
df_resultados_rj.to_csv('Dados Enem 2024 - RJ', sep=';', index = False)

# ANALISE

# dados da media das notas totais

def tendencia_central (a):
    # Calculo das medidas de tendencias centrais
        # formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
    media_notas= np.nanmean(a)
    mediana_notas= np.nanmedian(a)
    distancia_notas= ((media_notas - mediana_notas)/mediana_notas)*100
    print(f"Média: {media_notas:.2f}\nMediana: {mediana_notas:.2f}\nDistancia: {distancia_notas:.2f}% ")
    return

def outliers (b):
    # determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
    q1, q2, q3= np.nanpercentile(b , [25, 50, 75])
    iqr = q3 - q1
    limite_superior_notas = q3 + (1.5 * iqr)
    limite_inferior_notas = q1 - (1.5 * iqr)           
    print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}\nValores de corte:\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")
    return limite_inferior_notas, limite_superior_notas

tendencia_central(df_resultados_rj['NOTA_MEDIA'])
limite_inferior_notas, limite_superior_notas = outliers (np.array(df_resultados_rj['NOTA_MEDIA']))

#filtrando (pelo corte do quartil) os outliers +75
maior_25_enem = df_resultados_rj.loc[df_resultados_rj['NOTA_MEDIA'] >= limite_superior_notas]
#exibindo apenas as colunas especificas para analise
maior_25_enem = maior_25_enem[['NU_SEQUENCIAL', 'NOTA_MEDIA']].sort_values(by='NOTA_MEDIA', ascending=False).head()
maior_25_enem

#filtrando (pelo corte do quartil) os outliers -25
menor_25_enem = df_resultados_rj.loc[df_resultados_rj['NOTA_MEDIA'] <= limite_inferior_notas]
# retirando todas as provas zeradas
menor_25_enem = menor_25_enem[menor_25_enem['NOTA_MEDIA'] != 0]
# exibindo apenas as colunas especificas para analise
menor_25_enem = menor_25_enem[['NU_SEQUENCIAL', 'NOTA_MEDIA']].sort_values(by='NOTA_MEDIA', ascending=False).tail(5)
menor_25_enem

# dados das notas de ciencias da natureza
tendencia_central(df_resultados_rj['NU_NOTA_CN'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_resultados_rj['NU_NOTA_CN']))

# dados das notas de ciencias humanas
tendencia_central(df_resultados_rj['NU_NOTA_CH'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_resultados_rj['NU_NOTA_CH']))

# dados das notas de linguagens e codigos
tendencia_central(df_resultados_rj['NU_NOTA_LC'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_resultados_rj['NU_NOTA_LC']))

# filtro para separar as provas de ingles e espanhol
df_notas_ing = df_resultados.loc[df_resultados['TP_LINGUA'] == 0]
df_notas_esp = df_resultados.loc[df_resultados['TP_LINGUA'] == 1]

# dados das notas de linguagens e codigos - ingles (0)
    # Agrupando todas as notas de ingles
df_notas_ing = df_resultados_rj.loc[df_resultados_rj['TP_LINGUA'] == 0]

tendencia_central(df_notas_ing['NU_NOTA_LC'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_notas_ing['NU_NOTA_LC']))

# dados das notas de linguagens e codigos - espanhol (1)
    # Agrupando todas as notas de espanhol
df_notas_esp = df_resultados_rj.loc[df_resultados_rj['TP_LINGUA'] == 1]

tendencia_central(df_notas_esp['NU_NOTA_LC'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_notas_esp['NU_NOTA_LC']))

# dados das notas de matematica
tendencia_central(df_resultados_rj['NU_NOTA_MT'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_resultados_rj['NU_NOTA_MT']))

# dados das notas da redação
tendencia_central(df_resultados_rj['NU_NOTA_REDACAO'])
limite_inferior_notas, limite_superior_notas = outliers(np.array(df_resultados_rj['NU_NOTA_REDACAO']))

# criando boxplot em comparação para cada um das notas
# sintaxe para retirar os NaN das notas para que possamos exibi-las
data = df_resultados_rj.dropna(subset=['NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'])
data2 = df_notas_esp.dropna(subset= ['NU_NOTA_LC'])
data3 = df_notas_ing.dropna(subset= ['NU_NOTA_LC'])
#criando uma variavel para alocar para que possamos exibir no boxplot
notas = data['NU_NOTA_CH'],data['NU_NOTA_CN'], data['NU_NOTA_LC'], data2 ['NU_NOTA_LC'], data3 ['NU_NOTA_LC'], data['NU_NOTA_MT'], data['NU_NOTA_REDACAO'],
#definindo o tamanho do boxplot
fig, axs = plt.subplots(figsize=(15, 5))
# Creates grouped boxplots
plt.boxplot(notas, labels=['Ciencias Humanas', 'Ciencias da Natureza', 'Lingua e Codigos (Total)', 'Lingua e Codigos (Espanhol)', 'Lingua e Codigos (Ingles)','Matemática', 'Redação'], vert = False)
plt.title('Notas Boxplots')
plt.ylabel('\nMatérias')
plt.xlabel('\nNotas')
plt.grid(True)
plt.show()

# analise boxplot da nota media por inscrição

data4 = df_resultados_rj.dropna(subset=['NOTA_MEDIA'])
data4 = data4['NOTA_MEDIA']
fig, axs = plt.subplots(figsize=(15, 5))
plt.boxplot(data4, vert = False)
plt.title('Nota Media - Boxplot')
plt.ylabel('Valor')
plt.grid(True)
plt.show()

