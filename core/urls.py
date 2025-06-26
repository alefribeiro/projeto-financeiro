from django.urls import path
from core.views.fornecedor import FornecedorView
from core.views.lancamento import (
    LancamentoViewSet
)


urlpatterns = [
    path('fornecedor/', FornecedorView.as_view(), name='fornecedor_list'),
    path('fornecedor/<int:pk>/', FornecedorView.as_view(), name='fornecedor_detail'),
     path('lancamentos', view=LancamentoViewSet.as_view()),
    path('lancamentos/<int:pk>', view=LancamentoViewSet.as_view()),
]