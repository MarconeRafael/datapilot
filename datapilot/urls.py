from django.contrib import admin
from django.urls import path, include
from . import views  # Certifique-se de que sua view home está importada corretamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Página inicial
    path('tratamento/', include('tratamento.urls')),  
]
