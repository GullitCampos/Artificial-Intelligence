import os 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def obter_numero_vizinho_proximo():
    while True:
        try:
            vizinho_proximo = int(input("Escolha o número de vizinhos próximos (entre 1 e 10): "))
            if 1 <= vizinho_proximo <= 10:
                return vizinho_proximo
            else:
                print("Por favor, insira um número entre 1 e 10.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")

def plotar_metodo_cotovelo(variaveis_independentes, variavel_dependente):
    distorcoes = []
    for vizinho_proximo in range(1, 11):
        knn = KNeighborsClassifier(n_neighbors=vizinho_proximo)
        knn.fit(variaveis_independentes, variavel_dependente)
        distorcoes.append(np.mean(knn.predict(variaveis_independentes) != variavel_dependente))

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 11), distorcoes, 'bo-', markersize=8)
    plt.xlabel('Número de Vizinhos (vizinho_proximo)', fontsize=14)
    plt.ylabel('Erro de Classificação Médio', fontsize=14)
    plt.title('Método do Cotovelo para Encontrar o Número Ideal de Vizinhos (vizinho_proximo)', fontsize=16)
    plt.grid(True)
    plt.xticks(range(1, 11))
    plt.show()

def plotar_dispersao_qualidade(dado):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    cores = {1: 'royalblue', 0: 'orange'}
    
    ax.scatter(dado['Size'], dado['Weight'], dado['Quality'], 
               c=dado['Quality'].map(cores), s=70, alpha=0.6, edgecolors='w', label='Qualidade')
    
    ax.set_xlabel('Size', fontsize=14)
    ax.set_ylabel('Weight', fontsize=14)
    ax.set_zlabel('Quality', fontsize=14)
    ax.set_title('Gráfico de Dispersão 3D: Qualidade do morango', fontsize=16)
    
    plt.legend(['Bom', 'Ruim'], loc='upper left')
    plt.grid(True)
    plt.show()

def plotar_matriz_confusao(matriz_confusao):
    plt.figure(figsize=(8, 6))
    sns.heatmap(matriz_confusao, annot=True, cmap="Blues", fmt="d")
    plt.title("Matriz de Confusão", fontsize=16)
    plt.xlabel("Previsto", fontsize=14)
    plt.ylabel("Real", fontsize=14)
    plt.show()

def executar_knn_com_exclusao_colunas(dado, vizinho_proximo):
    colunas_para_excluir = dado.columns.difference(['A_id', 'Quality'])
    matriz_confusao_final = None  # Variável para armazenar a última matriz de confusão

    for coluna in colunas_para_excluir:
        print("\nExcluindo a coluna:", coluna)
        previsoes, matriz_confusao, acuracia, precisao, revocacao, especificidade = testes_knn(dado.drop(columns=[coluna]), vizinho_proximo)
        matriz_confusao_final = matriz_confusao  # Armazena a matriz de confusão

    if matriz_confusao_final is not None:
        plotar_matriz_confusao(matriz_confusao_final)  # Plota apenas a última matriz de confusão

def testes_knn(dado, vizinho_proximo):
    variaveis_independentes = dado.drop(columns=['A_id', 'Quality'])
    variavel_dependente = dado['Quality']
    variaveis_independentes = (variaveis_independentes - variaveis_independentes.min()) / (variaveis_independentes.max() - variaveis_independentes.min())
    normalizado = variaveis_independentes.join(variavel_dependente)
    print("Matriz normalizada:")
    print(normalizado)

    tamanho_treino = int((70 / 100) * len(dado))
    variaveis_independentes_treino, variaveis_independentes_teste = variaveis_independentes[:tamanho_treino], variaveis_independentes[tamanho_treino:]
    variavel_dependente_treino, variavel_dependente_teste = variavel_dependente[:tamanho_treino], variavel_dependente[tamanho_treino:]

    previsoes = []
    for indice_teste in range(len(variaveis_independentes_teste)):
        distancias = np.sqrt(np.sum((variaveis_independentes_treino - variaveis_independentes_teste.iloc[indice_teste]) ** 2, axis=1))
        vizinhos_mais_proximos = distancias.argsort()[:vizinho_proximo]
        rotulos_mais_proximos = variavel_dependente_treino.iloc[vizinhos_mais_proximos]
        rotulo_mais_comum = rotulos_mais_proximos.mode()[0]
        previsoes.append(rotulo_mais_comum)

    matriz_confusao = confusion_matrix(variavel_dependente_teste, previsoes)
    acuracia = accuracy_score(variavel_dependente_teste, previsoes)
    precisao = matriz_confusao[0][0] / (matriz_confusao[0][0] + matriz_confusao[1][0]) if (matriz_confusao[0][0] + matriz_confusao[1][0]) > 0 else 0
    revocacao = matriz_confusao[0][0] / (matriz_confusao[0][0] + matriz_confusao[0][1]) if (matriz_confusao[0][0] + matriz_confusao[0][1]) > 0 else 0
    especificidade = matriz_confusao[1][1] / (matriz_confusao[1][1] + matriz_confusao[1][0]) if (matriz_confusao[1][1] + matriz_confusao[1][0]) > 0 else 0

    print(matriz_confusao)
    print("Acurácia:", ((previsoes == variavel_dependente_teste).mean() * 100), "%")
    print("Precisão: ", precisao * 100, " %")
    print("Revocação: ", revocacao * 100, " %")
    print("Especificidade: ", especificidade * 100, " %")

    return previsoes, matriz_confusao, acuracia, precisao, revocacao, especificidade

def ler_arquivo_csv(caminho_arquivo):
    try:
        dados = pd.read_csv(caminho_arquivo)
        return dados
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Erro: ", e)
        return None

def tratar_dataset(dado):
    dado['Quality'] = dado['Quality'].replace({'good': 1, 'bad': 0})
    dado.dropna(inplace=True)
    dado['Acidity'] = dado['Acidity'].astype(float)
    dado['Quality'] = dado['Quality'].astype(int)
    dado.info()
    return dado

def main():
    caminho_arquivo = 'qualidade_morango.csv'
    morango = ler_arquivo_csv(caminho_arquivo)
    
    if morango is not None:
        morango = tratar_dataset(morango)
        vizinho_proximo = obter_numero_vizinho_proximo()  
        
        plotar_metodo_cotovelo(morango.drop(columns=['A_id', 'Quality']), morango['Quality'])
        plotar_dispersao_qualidade(morango)
        executar_knn_com_exclusao_colunas(morango, vizinho_proximo)
        
if __name__ == "__main__":
    main()
