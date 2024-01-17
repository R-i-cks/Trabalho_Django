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
    path("medicamento/<int:id>/", views.MedicamentoView.as_view(), name="medicamento"),
    path("utentes/", ListaUtentesView.as_view(), name="utentes"),
    path("consultas/", ListaConsultasView.as_view(), name="consultas"),
    path("medicos/", ListaMedicosView.as_view(), name="medicos"),
    path("enfermeiros/", ListaEnfermeirosView.as_view(), name="enfermeiros"),
    path("medicamentos/", ListaMedicamentosView.as_view(), name="medicamentos"),
    path("familiares/", ListaFamiliaresView.as_view(), name="familiares"),
    path('add_consulta/<int:id>/', views.add_consulta, name='add_consulta'),
    path('add_utente/<int:id>/', views.add_utente, name='add_utente'),
    path('add_medico/<int:id>/', views.add_medico, name='add_medico'),
    path('add_enfermeiro/<int:id>/', views.add_enfermeiro, name='add_enfermeiro'),
    path('add_medicamento/<int:id>/', views.add_medicamento, name='add_medicamento'),
    path('add_familiar/<int:id>/', views.add_familiar, name='add_familiar'),
    path('add_prescricao/<int:consulta_id>/<int:medico_id>/<int:utente_id>/', views.add_prescricao, name='add_prescricao'),
    path('add_medicao/<int:consulta_id>/<int:medico_id>/<int:utente_id>/', views.add_medicao, name='add_medicao'),
    path('add_exame/<int:consulta_id>/<int:medico_id>/<int:utente_id>/', views.add_exame, name='add_exame'),

    path("logout/", views.logout_view, name="logout"),
]
