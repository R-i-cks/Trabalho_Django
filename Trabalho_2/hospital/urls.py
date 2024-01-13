from django.urls import path, include

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.home, name="home"),
    path("user_login/",views.user_login, name="user_login"),
    path('utente/<int:id>/', views.UtenteView.as_view(), name='utente'),
    path('medico/<int:id>/', views.MedicoView.as_view(), name='medico'),
    path('medico/<int:medico_id>/create-consulta/', views.ConsultaCreateView.as_view(), name='consulta_create'),
    path('logout/', views.logout_view, name='logout'),
]