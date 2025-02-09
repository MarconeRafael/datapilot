from django.shortcuts import render

def home(request):
    """
    View para a página inicial do projeto.
    """
    return render(request, "index.html")
