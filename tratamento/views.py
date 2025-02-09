from django.shortcuts import render
import pandas as pd
import logging
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

def carregar_dataset(request):
    """Recupera e converte o dataset salvo na sessão"""
    dataset = request.session.get("dataset")
    return pd.DataFrame.from_dict(dataset) if dataset else None

def receber_dados(request):
    """Recebe o arquivo CSV enviado pelo usuário e armazena na sessão"""
    contexto = {}
    
    if request.method == "POST" and request.FILES.get("arquivo"):
        arquivo = request.FILES["arquivo"]
        
        try:
            dataset = ler_arquivo_csv(arquivo)
            request.session["dataset"] = dataset.to_dict()
            request.session["variaveis"] = obter_variaveis(dataset)
            contexto["mensagem"] = "✅ Arquivo carregado com sucesso!"
            logging.info("Arquivo CSV carregado e armazenado na sessão.")
        except Exception as e:
            contexto["erro"] = f"❌ Erro ao carregar arquivo: {e}"
            logging.error(f"Erro ao carregar arquivo CSV: {e}")
    
    return render(request, "receber_dados.html", contexto)

def exibir_coisas(request):
    """Executa funções de exibição de dados e renderiza os resultados"""
    contexto = {}
    dataset = carregar_dataset(request)

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
                logging.info(f"Função '{funcao}' executada com sucesso.")
            else:
                contexto["erro"] = "❌ Função inválida."
        
        except Exception as e:
            contexto["erro"] = f"❌ Erro ao processar função: {e}"
            logging.error(f"Erro ao processar '{funcao}': {e}")

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
            
            elif funcao == "calcular_correlacao":
                contexto["resultado"] = calcular_correlacao(dataset).to_html()
            
            elif funcao == "correlacao_com_variavel":
                variavel = request.POST.get("variavel")
                contexto["resultado"] = correlacao_com_variavel(dataset, variavel).to_frame().to_html()
            
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
                plotar_histograma(dataset, variavel)
            
            else:
                contexto["erro"] = "❌ Função inválida."
        
        except Exception as e:
            contexto["erro"] = f"❌ Erro ao processar função: {e}"
            logging.error(f"Erro ao processar '{funcao}': {e}")

    return render(request, "fazer_operacoes.html", contexto)


def dividir_dados_treino_teste_operacao(dataset, request):
    """Auxiliar para dividir os dados em treino e teste"""
    variaveis = request.POST.get("variaveis").split(",")
    X = dataset[variaveis]
    Y = dataset[request.POST.get("variavel")]
    X_train, X_test, Y_train, Y_test = dividir_dados_treino_teste(X, Y)
    return f"✅ Divisão concluída: X_train: {X_train.shape}, X_test: {X_test.shape}"

def padronizar_dados_operacao(dataset, request):
    """Auxiliar para padronizar os dados"""
    variaveis = request.POST.get("variaveis").split(",")
    X = dataset[variaveis]
    Y = dataset[request.POST.get("variavel")]
    X_train, X_test, _, _ = dividir_dados_treino_teste(X, Y)
    X_train_scaled, X_test_scaled = padronizar_dados(X_train, X_test)
    return "✅ Padronização concluída."
