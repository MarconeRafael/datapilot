from django.urls import path
from . import views  # Certifique-se de que a view tratada está importada corretamente

urlpatterns = [
    path('', views.tratamento_view, name='home'),  # Substitua home por tratamento_view
]
