from django.urls import path
from . import views
app_name = 'tratamento'
urlpatterns = [
    path('receber_dados/', views.receber_dados, name='receber_dados'),
    path('exibir_coisas/', views.exibir_coisas, name='exibir_coisas'),
    path('fazer_operacoes/', views.fazer_operacoes, name='fazer_operacoes'),
]
