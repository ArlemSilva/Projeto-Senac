import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# TRATAMENTO
#df_prova = pd.read_csv('ITENS_PROVA_2024.csv', sep = ';', encoding = 'latin1')
#df_participantes = pd.read_csv('PARTICIPANTES_2024.csv', sep = ';', encoding = 'latin1')
df_resultados = pd.read_csv('RESULTADOS_2024.csv', sep = ';', encoding = 'latin1')

# filtro para apenas no estado do Rio de Janeiro
df_resultados_rj = df_resultados.loc[df_resultados['SG_UF_ESC'] == 'RJ']

# eliminando as colunas dos gabaritos e respostas dos participantes
df_resultados_rj = df_resultados_rj.drop(columns = ['TX_RESPOSTAS_CN','TX_RESPOSTAS_CH','TX_RESPOSTAS_LC','TX_RESPOSTAS_MT','TX_GABARITO_CN','TX_GABARITO_CH','TX_GABARITO_LC','TX_GABARITO_MT'], axis = 1)

# eliminando as colunas dos codigos dos tipos de provas
df_resultados_rj = df_resultados_rj.drop(columns = ['CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC',], axis = 1)

# eliminando as colunas com os codigos do municipio da escola e codigo do estado da onde foi aplicado a prova
df_resultados_rj = df_resultados_rj.drop(columns = ['CO_MUNICIPIO_ESC', 'CO_UF_ESC'], axis = 1)

# transformando o Data Frame tratado para csv (para utilizar no power bi e analisar com  graficos)
df_resultados_rj.to_csv('Dados Enem 2024 - RJ', sep=';', index = False)

# ANALISE
# filtro para separar as provas de ingles e espanhol
df_notas_idioma = df_resultados_rj.groupby('TP_LINGUA')['NU_NOTA_LC'].mean().reset_index()
df_notas_ing = df_resultados.loc[df_resultados['TP_LINGUA'] == 0]
df_notas_esp = df_resultados.loc[df_resultados['TP_LINGUA'] == 1]

# criando uma nova coluna com o valor da media das notas dos inscritos
df_resultados_rj['NOTA_MEDIA'] = df_resultados_rj[['NU_NOTA_CN','NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis = 1)

# dados da media das notas totais
# Calculo das medidas de tendencias centrais
dados_notas_rj = np.array(df_resultados_rj['NOTA_MEDIA'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas= np.nanmean(df_resultados_rj['NOTA_MEDIA'])
mediana_notas= np.nanmedian(df_resultados_rj['NOTA_MEDIA'])
distancia_notas= (media_notas - mediana_notas)/mediana_notas
distancia_notas = distancia_notas*100
print(f"Média: {media_notas:.2f}\nMediana: {mediana_notas:.2f}\nDistancia: {distancia_notas:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_rj,25) 
q2= np.nanpercentile(dados_notas_rj,50) 
q3= np.nanpercentile(dados_notas_rj,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

#filtrando (pelo corte do quartil) os outliers +75
maior_25_enem = df_resultados_rj.loc[df_resultados_rj['NOTA_MEDIA'] >= q3 ]
#exibindo apenas as colunas especificas para analise
maior_25_enem = maior_25_enem[['NU_SEQUENCIAL', 'NOTA_MEDIA']].sort_values(by='NOTA_MEDIA', ascending=False).head(10)
maior_25_enem

#filtrando (pelo corte do quartil) os outliers -25
menor_25_enem = df_resultados_rj.loc[df_resultados_rj['NOTA_MEDIA'] <= q1]
# retirando todas as provas zeradas
menor_25_enem = menor_25_enem[menor_25_enem['NOTA_MEDIA'] != 0]
# exibindo apenas as colunas especificas para analise
menor_25_enem = menor_25_enem[['NU_SEQUENCIAL', 'NOTA_MEDIA']].sort_values(by='NOTA_MEDIA', ascending=False).tail(10)
menor_25_enem

# dados das notas de ciencias da natureza
# Calculo das medidas de tendencias centrais
dados_notas_cn = np.array(df_resultados_rj['NU_NOTA_CN'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_cn= np.nanmean(df_resultados_rj['NU_NOTA_CN'])
mediana_notas_cn= np.nanmedian(df_resultados_rj['NU_NOTA_CN'])
distancia_notas_cn= (media_notas_cn - mediana_notas_cn)/mediana_notas_cn
distancia_notas_cn = distancia_notas_cn*100
print(f"Média: {media_notas_cn:.2f}\nMediana: {mediana_notas_cn:.2f}\nDistancia: {distancia_notas_cn:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_cn,25) 
q2= np.nanpercentile(dados_notas_cn,50) 
q3= np.nanpercentile(dados_notas_cn,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas de ciencias humanas
# Calculo das medidas de tendencias centrais
dados_notas_ch = np.array(df_resultados_rj['NU_NOTA_CH'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_ch= np.nanmean(df_resultados_rj['NU_NOTA_CH'])
mediana_notas_ch= np.nanmedian(df_resultados_rj['NU_NOTA_CH'])
distancia_notas_ch= (media_notas_ch - mediana_notas_ch)/mediana_notas_ch
distancia_notas_ch = distancia_notas_ch*100
print(f"Média: {media_notas_ch:.2f}\nMediana: {mediana_notas_ch:.2f}\nDistancia: {distancia_notas_ch:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_ch,25) 
q2= np.nanpercentile(dados_notas_ch,50) 
q3= np.nanpercentile(dados_notas_ch,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas de linguagens e codigos
# Calculo das medidas de tendencias centrais
dados_notas_lc = np.array(df_resultados_rj['NU_NOTA_LC'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_lc= np.nanmean(df_resultados_rj['NU_NOTA_LC'])
mediana_notas_lc= np.nanmedian(df_resultados_rj['NU_NOTA_LC'])
distancia_notas_lc= (media_notas_lc - mediana_notas_lc)/mediana_notas_lc
distancia_notas_lc = distancia_notas_lc*100
print(f"Média: {media_notas_lc:.2f}\nMediana: {mediana_notas_lc:.2f}\nDistancia: {distancia_notas_lc:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_lc,25) 
q2= np.nanpercentile(dados_notas_lc,50) 
q3= np.nanpercentile(dados_notas_lc,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas de linguagens e codigos - ingles (0)
# Calculo das medidas de tendencias centrais
dados_notas_ing = np.array(df_notas_ing['NU_NOTA_LC'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_ing= np.nanmean(df_notas_ing['NU_NOTA_LC'])
mediana_notas_ing= np.nanmedian(df_notas_ing['NU_NOTA_LC'])
distancia_notas_ing= (media_notas_ing - mediana_notas_ing)/mediana_notas_ing
distancia_notas_ing = distancia_notas_ing*100
print(f"Média: {media_notas_ing:.2f}\nMediana: {mediana_notas_ing:.2f}\nDistancia: {distancia_notas_ing:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_ing,25) 
q2= np.nanpercentile(dados_notas_ing,50) 
q3= np.nanpercentile(dados_notas_ing,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas de linguagens e codigos - espanhol (1)
# Calculo das medidas de tendencias centrais
dados_notas_lc = np.array(df_notas_esp['NU_NOTA_LC'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_lc= np.nanmean(df_notas_esp['NU_NOTA_LC'])
mediana_notas_lc= np.nanmedian(df_notas_esp['NU_NOTA_LC'])
distancia_notas_lc= (media_notas_lc - mediana_notas_lc)/mediana_notas_lc
distancia_notas_lc = distancia_notas_lc*100
print(f"Média: {media_notas_lc:.2f}\nMediana: {mediana_notas_lc:.2f}\nDistancia: {distancia_notas_lc:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_lc,25) 
q2= np.nanpercentile(dados_notas_lc,50) 
q3= np.nanpercentile(dados_notas_lc,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas de matematica
# Calculo das medidas de tendencias centrais
dados_notas_mt = np.array(df_resultados_rj['NU_NOTA_MT'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_mt= np.nanmean(df_resultados_rj['NU_NOTA_MT'])
mediana_notas_mt= np.nanmedian(df_resultados_rj['NU_NOTA_MT'])
distancia_notas_mt= (media_notas_mt - mediana_notas_mt)/mediana_notas_mt
distancia_notas_mt = distancia_notas_mt*100
print(f"Média: {media_notas_mt:.2f}\nMediana: {mediana_notas_mt:.2f}\nDistancia: {distancia_notas_mt:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_mt,25) 
q2= np.nanpercentile(dados_notas_mt,50) 
q3= np.nanpercentile(dados_notas_mt,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

# dados das notas da redação
# Calculo das medidas de tendencias centrais
dados_notas_rd = np.array(df_resultados_rj['NU_NOTA_REDACAO'])
# formula 'nanmean' e 'nanmedian' para ignorar os valores NaN e fazer os calculos
media_notas_rd= np.nanmean(df_resultados_rj['NU_NOTA_REDACAO'])
mediana_notas_rd= np.nanmedian(df_resultados_rj['NU_NOTA_REDACAO'])
distancia_notas_rd= (media_notas_rd - mediana_notas_rd)/mediana_notas_rd
distancia_notas_rd = distancia_notas_rd*100
print(f"Média: {media_notas_rd:.2f}\nMediana: {mediana_notas_rd:.2f}\nDistancia: {distancia_notas_rd:.2f}%")
# determinando os quartis, usando a formula 'nanpercertile' para ignorar os valores NaN e fazer os calculos
q1= np.nanpercentile(dados_notas_rd,25) 
q2= np.nanpercentile(dados_notas_rd,50) 
q3= np.nanpercentile(dados_notas_rd,75) 
print(f"Quartis\nQ1: {q1:.2f}\nQ2: {q2:.2f}\nQ3: {q3:.2f}")
iqr = q3 - q1
limite_superior_notas = q3 + (1.5 * iqr)
limite_inferior_notas = q1 - (1.5 * iqr)
print(f"Valores de corte\nLimite superior: {limite_superior_notas:.2f}\nLimite inferior: {limite_inferior_notas:.2f}")

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

# transformando o Data Frame tratado para csv (para utilizar no power bi e analisar com  graficos)
df_resultados_rj.to_csv('Dados Provas Enem 2024 - RJ.csv', sep=';', index = False)