from django.urls import path

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/utente/", views.UtenteView.as_view(), name="utente"),
    path("<int:pk>/medico/", views.MedicoView.as_view(), name="medico"),
    path("<int:pk>/medicamento/", views.MedicamentoView.as_view(), name="medicamento"),
    path("<int:pk>/consulta/", views.ConsultaView.as_view(), name="consulta"),
]