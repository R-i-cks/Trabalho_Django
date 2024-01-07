from django.urls import path, include

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('detail/<int:id>/', views.DetailView.as_view(), name='detail'),
    path('utente/<int:id>/', views.UtenteView.as_view(), name='utente'),
    path('medico/<int:id>/', views.MedicoView.as_view(), name='medico'),
]