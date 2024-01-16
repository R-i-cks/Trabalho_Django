from django.urls import path, include
from .views import (
    ListaUtentesView,
    ListaConsultasView,
    ListaMedicosView,
    ListaEnfermeirosView,
    ListaMedicamentosView,
    ListaFamiliaresView,
)

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.home, name="home"),
    path("user_login/", views.user_login, name="user_login"),
    path("utente/<int:id>/", views.UtenteView.as_view(), name="utente"),
    path("medico/<int:id>/", views.MedicoView.as_view(), name="medico"),
    path("familiar/<int:id>/", views.FamiliarView.as_view(), name="familiar"),
    path("auxiliar/<int:id>/", views.AuxiliarView.as_view(), name="auxiliar"),
    path("enfermeiro/<int:id>/", views.EnfermeiroView.as_view(), name="enfermeiro"),
    path("index_auxiliar/", views.IndexAuxiliarView.as_view(), name="index_auxiliar"),
    path("utentes/", ListaUtentesView.as_view(), name="utentes"),
    path("consultas/", ListaConsultasView.as_view(), name="consultas"),
    path("medicos/", ListaMedicosView.as_view(), name="medicos"),
    path("enfermeiros/", ListaEnfermeirosView.as_view(), name="enfermeiros"),
    path("medicamentos/", ListaMedicamentosView.as_view(), name="medicamentos"),
    path("familiares/", ListaFamiliaresView.as_view(), name="familiares"),
    path("logout/", views.logout_view, name="logout"),
]
