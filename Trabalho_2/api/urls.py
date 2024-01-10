from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.getData),
    path('add/', views.addConsulta), #Endpoint
    path('utente', views.UtenteView.as_view( ),name='utente')
]