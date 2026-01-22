from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar_transacao, name='adicionar_transacao'),
    path('excluir/<int:id>/', views.excluir_transacao, name='excluir_transacao'),
]