from django.urls import path
from core import views

urlpatterns = [
    path('fornecedor/', views.fornecedor_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
]