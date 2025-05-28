from django.urls import path
from core.views.fornecedor import FornecedorView


urlpatterns = [
    path('fornecedor/', FornecedorView.as_view(), name='fornecedor_list'),
    path('fornecedor/<int:pk>/', FornecedorView.as_view(), name='fornecedor_detail'),
]