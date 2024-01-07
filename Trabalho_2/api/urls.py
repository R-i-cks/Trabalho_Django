from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/', views.addConsulta), #Endpoint
    path('utente', views.UtenteView.as_view( ),name='utente')
]