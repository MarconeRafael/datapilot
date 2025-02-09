import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ler_arquivo_csv(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna um DataFrame do Pandas.

    :param caminho_arquivo: str - Caminho do arquivo CSV.
    :return: pd.DataFrame - DataFrame carregado.
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        logging.info("Arquivo CSV carregado com sucesso.")
        return df
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo CSV: {e}")
        raise

def exibir_info(dataset):
    """
    Exibe informações gerais sobre o DataFrame, incluindo o número de entradas, tipos de dados e valores nulos.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    """
    logging.info("Exibindo informações do DataFrame:")
    return dataset.info()

def exibir_head(dataset, n=5):
    """
    Retorna as primeiras 'n' linhas do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :param n: int - Número de linhas a exibir (padrão: 5).
    :return: pd.DataFrame - DataFrame contendo as primeiras linhas.
    """
    return dataset.head(n)

def exibir_describe(dataset):
    """
    Retorna estatísticas descritivas das colunas numéricas do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :return: pd.DataFrame - Estatísticas descritivas.
    """
    return dataset.describe()

def contar_valores_nulos(dataset):
    """
    Retorna a contagem de valores nulos para cada coluna do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :return: pd.Series - Contagem de valores nulos por coluna.
    """
    return dataset.isnull().sum()

def remover_valores_nulos(dataset):
    """
    Retorna um novo DataFrame com as linhas contendo valores nulos removidas.

    :param dataset: pd.DataFrame - Conjunto de dados original.
    :return: pd.DataFrame - Conjunto de dados sem valores nulos.
    """
    return dataset.dropna()

def calcular_correlacao(dataset):
    """
    Retorna a matriz de correlação entre as colunas numéricas do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :return: pd.DataFrame - Matriz de correlação.
    """
    return dataset.corr()

def plotar_heatmap_correlacao(dataset):
    """
    Plota um heatmap da matriz de correlação entre as colunas numéricas do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    """
    plt.figure(figsize=(16, 8))
    sns.heatmap(dataset.corr(), cmap='Reds', annot=True, fmt=".2f", linewidths=0.5)
    plt.title('Heatmap de Correlação')
    plt.show()

def correlacao_com_variavel(dataset, variavel):
    """
    Retorna a correlação de todas as colunas com uma variável específica.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :param variavel: str - Nome da variável de referência.
    :return: pd.Series - Correlação das colunas com a variável escolhida.
    """
    if variavel not in dataset.columns:
        raise ValueError(f"A variável '{variavel}' não existe no DataFrame.")
    return dataset.corr()[variavel].sort_values(ascending=False)

def filtrar_variaveis(dataset, variaveis):
    """
    Retorna um novo DataFrame contendo apenas as colunas especificadas.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :param variaveis: list - Lista de colunas a serem filtradas.
    :return: pd.DataFrame - Conjunto de dados com as colunas filtradas.
    """
    for var in variaveis:
        if var not in dataset.columns:
            raise ValueError(f"A variável '{var}' não existe no DataFrame.")
    return dataset[variaveis]

def plotar_histograma(dataset, variavel):
    """
    Plota um histograma para a variável especificada.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :param variavel: str - Nome da variável a ser plotada.
    """
    if variavel not in dataset.columns:
        raise ValueError(f"A variável '{variavel}' não existe no DataFrame.")
    sns.histplot(dataset[variavel], kde=True, stat='density', linewidth=0)
    plt.title(f'Distribuição de {variavel}')
    plt.show()

def dividir_dados_treino_teste(X, Y, test_size=0.2, random_state=42):
    """
    Divide os dados em conjuntos de treino e teste.

    :param X: pd.DataFrame - Variáveis independentes.
    :param Y: pd.Series - Variável dependente.
    :param test_size: float - Proporção do conjunto de teste (padrão: 20%).
    :param random_state: int - Semente para reprodução dos resultados.
    :return: tuple - Conjuntos de treino e teste (X_train, X_test, Y_train, Y_test).
    """
    return train_test_split(X, Y, test_size=test_size, random_state=random_state)

def padronizar_dados(X_train, X_test):
    """
    Aplica padronização (normalização Z-score) aos conjuntos de treino e teste.

    :param X_train: pd.DataFrame - Conjunto de treinamento.
    :param X_test: pd.DataFrame - Conjunto de teste.
    :return: tuple - Conjuntos padronizados (X_train_scaled, X_test_scaled).
    """
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def obter_variaveis(dataset):
    """
    Retorna a lista de colunas do DataFrame.

    :param dataset: pd.DataFrame - Conjunto de dados a ser analisado.
    :return: list - Lista de nomes das colunas.
    """
    return dataset.columns.tolist()
