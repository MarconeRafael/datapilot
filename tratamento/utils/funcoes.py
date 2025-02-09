import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def ler_arquivo_csv(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna um DataFrame do Pandas.
    """
    return pd.read_csv(caminho_arquivo)

def exibir_info(dataset):
    """
    Exibe informações gerais sobre o DataFrame, incluindo o número de entradas, tipos de dados e valores nulos.
    """
    dataset.info()

def exibir_head(dataset, n=5):
    """
    Exibe as primeiras 'n' linhas do DataFrame. O padrão é 5.
    """
    print(dataset.head(n))

def exibir_describe(dataset):
    """
    Exibe estatísticas descritivas das colunas numéricas do DataFrame.
    """
    print(dataset.describe())

def contar_valores_nulos(dataset):
    """
    Retorna a contagem de valores nulos para cada coluna do DataFrame.
    """
    return dataset.isnull().sum()

def remover_valores_nulos(dataset):
    """
    Retorna um novo DataFrame com as linhas contendo valores nulos removidas.
    """
    return dataset.dropna()

def calcular_correlacao(dataset):
    """
    Retorna a matriz de correlação entre as colunas numéricas do DataFrame.
    """
    return dataset.corr()

def plotar_heatmap_correlacao(dataset):
    """
    Plota um heatmap da matriz de correlação entre as colunas numéricas do DataFrame.
    """
    plt.figure(figsize=(16, 8))
    sns.heatmap(dataset.corr(), cmap='Reds', annot=True, fmt=".2f", linewidths=0.5)
    plt.title('Heatmap de Correlação')
    plt.show()

def correlacao_com_variavel(dataset, variavel):
    """
    Retorna a correlação de todas as colunas com uma variável específica.
    """
    if variavel not in dataset.columns:
        raise ValueError(f"A variável '{variavel}' não existe no DataFrame.")
    return dataset.corr()[variavel].sort_values(ascending=False)

def filtrar_variaveis(dataset, variaveis):
    """
    Retorna um novo DataFrame contendo apenas as colunas especificadas.
    """
    for var in variaveis:
        if var not in dataset.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")
    return dataset[variaveis]

def plotar_histograma(dataset, variavel):
    """
    Plota um histograma para a variável especificada.
    """
    if variavel not in dataset.columns:
        raise ValueError(f"A variável '{variavel}' não existe no DataFrame.")
    sns.histplot(dataset[variavel], kde=True, stat='density', linewidth=0)
    plt.title(f'Distribuição de {variavel}')
    plt.show()

def dividir_dados_treino_teste(X, Y, test_size=0.2, random_state=42):
    """
    Divide os dados em conjuntos de treino e teste.
    """
    return train_test_split(X, Y, test_size=test_size, random_state=random_state)

def padronizar_dados(X_train, X_test):
    """
    Aplica padronização (normalização Z-score) aos conjuntos de treino e teste.
    """
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled
