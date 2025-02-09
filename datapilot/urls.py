from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tratamento/', include('tratamento.urls')),  # Corrigido para evitar recursão
]
