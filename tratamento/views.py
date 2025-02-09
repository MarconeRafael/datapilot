from django.shortcuts import render
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
    padronizar_dados
)

def tratamento_view(request):
    contexto = {}

    if request.method == "POST" and request.FILES.get("arquivo"):
        arquivo = request.FILES["arquivo"]
        dataset = ler_arquivo_csv(arquivo)

        funcao = request.POST.get("funcao")

        try:
            if funcao == "exibir_info":
                exibir_info(dataset)
            elif funcao == "exibir_head":
                contexto["resultado"] = exibir_head(dataset, 5).to_html()
            elif funcao == "exibir_describe":
                contexto["resultado"] = exibir_describe(dataset).to_html()
            elif funcao == "contar_valores_nulos":
                contexto["resultado"] = contar_valores_nulos(dataset).to_frame().to_html()
            elif funcao == "remover_valores_nulos":
                dataset = remover_valores_nulos(dataset)
                contexto["resultado"] = dataset.head().to_html()
            elif funcao == "calcular_correlacao":
                contexto["resultado"] = calcular_correlacao(dataset).to_html()
            elif funcao == "plotar_heatmap_correlacao":
                plotar_heatmap_correlacao(dataset)
            elif funcao == "correlacao_com_variavel":
                variavel = request.POST.get("variavel")
                contexto["resultado"] = correlacao_com_variavel(dataset, variavel).to_frame().to_html()
            elif funcao == "filtrar_variaveis":
                variaveis = request.POST.get("variaveis").split(",")
                contexto["resultado"] = filtrar_variaveis(dataset, variaveis).head().to_html()
            elif funcao == "plotar_histograma":
                variavel = request.POST.get("variavel")
                plotar_histograma(dataset, variavel)
            elif funcao == "dividir_dados_treino_teste":
                variaveis = request.POST.get("variaveis").split(",")
                X = dataset[variaveis]
                Y = dataset[request.POST.get("variavel")]
                X_train, X_test, Y_train, Y_test = dividir_dados_treino_teste(X, Y)
                contexto["resultado"] = f"Divisão concluída: X_train: {X_train.shape}, X_test: {X_test.shape}"
            elif funcao == "padronizar_dados":
                variaveis = request.POST.get("variaveis").split(",")
                X = dataset[variaveis]
                Y = dataset[request.POST.get("variavel")]
                X_train, X_test, _, _ = dividir_dados_treino_teste(X, Y)
                X_train_scaled, X_test_scaled = padronizar_dados(X_train, X_test)
                contexto["resultado"] = "Padronização concluída."

        except Exception as e:
            contexto["erro"] = str(e)

    return render(request, "home.html", contexto)
