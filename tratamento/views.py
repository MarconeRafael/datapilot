import os
import time
import pandas as pd
import logging
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils.funcoes import (
    ler_arquivo_csv,
    exibir_info,
    exibir_head,
    exibir_describe,
    contar_valores_nulos,
    remover_valores_nulos,
    calcular_correlacao,
    plotar_heatmap_correlacao,
    correlacao_com_variavel,
    filtrar_variaveis,
    plotar_histograma,
    dividir_dados_treino_teste,
    padronizar_dados,
    obter_variaveis
)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# Tempo de expiração do arquivo na sessão (em segundos)
EXPIRACAO_ARQUIVO = 10 * 60  # 10 minutos

def carregar_dataset(request):
    """Recupera e converte o dataset salvo na sessão, verificando a expiração"""
    dataset = request.session.get("dataset")
    timestamp = request.session.get("timestamp")

    # Se o dataset existir, verifica o tempo de expiração
    if dataset and timestamp:
        tempo_atual = time.time()
        if tempo_atual - timestamp > EXPIRACAO_ARQUIVO:
            logging.info("⏳ O tempo expirou! Removendo arquivo da sessão.")
            request.session.pop("dataset", None)
            request.session.pop("timestamp", None)
            request.session.pop("variaveis", None)
            return None  # Retorna None para indicar que expirou

    return pd.DataFrame.from_dict(dataset) if dataset else None

def receber_dados(request):
    """Recebe o arquivo CSV enviado pelo usuário e armazena temporariamente na sessão"""
    contexto = {}

    if request.method == "POST" and request.FILES.get("arquivo"):
        arquivo = request.FILES["arquivo"]
        
        try:
            # Verifica se o formato é CSV
            if not arquivo.name.endswith(".csv"):
                raise ValueError("Formato inválido. Apenas arquivos CSV são permitidos.")

            # Verifica tamanho do arquivo (máximo 5MB)
            if arquivo.size > 5 * 1024 * 1024:
                raise ValueError("O arquivo é muito grande! O limite é de 5MB.")

            # Processa o arquivo
            dataset = ler_arquivo_csv(arquivo)

            if dataset is None or dataset.empty:
                raise ValueError("O dataset está vazio ou não foi carregado corretamente.")

            # Armazena na sessão
            request.session["dataset"] = dataset.to_dict()
            request.session["timestamp"] = time.time()
            request.session["variaveis"] = list(dataset.columns)

            contexto["mensagem"] = "✅ Arquivo carregado com sucesso!"
            print("DEBUG: Dados salvos na sessão:", request.session["dataset"])

        except Exception as e:
            contexto["erro"] = f"❌ Erro ao carregar arquivo: {e}"
            print("DEBUG: Erro no upload:", e)

    return render(request, "receber_dados.html", contexto)

def exibir_coisas(request):
    """Executa funções de exibição de dados e renderiza os resultados"""
    contexto = {}
    dataset = carregar_dataset(request)

    print("DEBUG: Dados carregados na página de exibição:", dataset)

    if dataset is not None:
        funcao = request.POST.get("funcao")
        
        try:
            resultado_map = {
                "exibir_info": lambda: exibir_info(dataset),
                "exibir_head": lambda: exibir_head(dataset, 5).to_html(),
                "exibir_describe": lambda: exibir_describe(dataset).to_html(),
                "contar_valores_nulos": lambda: contar_valores_nulos(dataset).to_frame().to_html(),
            }
            
            if funcao in resultado_map:
                contexto["resultado"] = resultado_map[funcao]()
                print("DEBUG: Função executada:", funcao)
            else:
                contexto["erro"] = "❌ Função inválida."
        
        except Exception as e:
            contexto["erro"] = f"❌ Erro ao processar função: {e}"
            print("DEBUG: Erro ao processar função:", e)

    return render(request, "exibir_coisas.html", contexto)


def fazer_operacoes(request):
    """Executa operações sobre os dados e renderiza os resultados"""
    contexto = {}
    dataset = carregar_dataset(request)
    
    if dataset is not None:
        funcao = request.POST.get("funcao")

        try:
            if funcao == "remover_valores_nulos":
                dataset = remover_valores_nulos(dataset)  # Atualiza dataset
                request.session["dataset"] = dataset.to_dict()  # Salva na sessão
                contexto["resultado"] = dataset.head().to_html()
                logging.info("Valores nulos removidos.")

            elif funcao == "calcular_correlacao":
                contexto["resultado"] = calcular_correlacao(dataset).to_html()

            elif funcao == "correlacao_com_variavel":
                variavel = request.POST.get("variavel")
                if variavel in dataset.columns:
                    contexto["resultado"] = correlacao_com_variavel(dataset, variavel).to_frame().to_html()
                else:
                    contexto["erro"] = "Variável não encontrada no dataset."

            elif funcao == "filtrar_variaveis":
                variaveis = request.POST.get("variaveis").split(",")
                dataset = filtrar_variaveis(dataset, variaveis)  # Atualiza dataset
                request.session["dataset"] = dataset.to_dict()  # Salva na sessão
                contexto["resultado"] = dataset.head().to_html()

            elif funcao == "dividir_dados_treino_teste":
                contexto["resultado"] = dividir_dados_treino_teste_operacao(dataset, request)

            elif funcao == "padronizar_dados":
                contexto["resultado"] = padronizar_dados_operacao(dataset, request)

            elif funcao == "plotar_heatmap_correlacao":
                plotar_heatmap_correlacao(dataset)

            elif funcao == "plotar_histograma":
                variavel = request.POST.get("variavel")
                if variavel in dataset.columns:
                    plotar_histograma(dataset, variavel)
                else:
                    contexto["erro"] = "Variável não encontrada no dataset."

            else:
                contexto["erro"] = "❌ Função inválida."
        
        except Exception as e:
            contexto["erro"] = f"❌ Erro ao processar função: {e}"
            logging.error(f"Erro ao processar '{funcao}': {e}")

    return render(request, "fazer_operacoes.html", contexto)


def dividir_dados_treino_teste_operacao(dataset, request):
    """Auxiliar para dividir os dados em treino e teste"""
    try:
        variaveis = request.POST.get("variaveis").split(",")
        if not set(variaveis).issubset(dataset.columns):
            return "❌ Algumas variáveis selecionadas não estão no dataset."

        X = dataset[variaveis]
        Y = dataset[request.POST.get("variavel")]

        if Y.name not in dataset.columns:
            return "❌ A variável alvo não foi encontrada no dataset."

        X_train, X_test, Y_train, Y_test = dividir_dados_treino_teste(X, Y)
        request.session["X_train"] = X_train.to_dict()
        request.session["X_test"] = X_test.to_dict()
        request.session["Y_train"] = Y_train.to_dict()
        request.session["Y_test"] = Y_test.to_dict()

        return f"✅ Divisão concluída: X_train: {X_train.shape}, X_test: {X_test.shape}"

    except Exception as e:
        logging.error(f"Erro ao dividir dados: {e}")
        return f"❌ Erro ao dividir dados: {e}"

def padronizar_dados_operacao(dataset, request):
    """Auxiliar para padronizar os dados"""
    try:
        variaveis = request.POST.get("variaveis").split(",")
        if not set(variaveis).issubset(dataset.columns):
            return "❌ Algumas variáveis selecionadas não estão no dataset."

        X = dataset[variaveis]
        Y = dataset[request.POST.get("variavel")]

        if Y.name not in dataset.columns:
            return "❌ A variável alvo não foi encontrada no dataset."

        X_train, X_test, _, _ = dividir_dados_treino_teste(X, Y)
        X_train_scaled, X_test_scaled = padronizar_dados(X_train, X_test)

        return "✅ Padronização concluída."

    except Exception as e:
        logging.error(f"Erro ao padronizar dados: {e}")
        return f"❌ Erro ao padronizar dados: {e}"
