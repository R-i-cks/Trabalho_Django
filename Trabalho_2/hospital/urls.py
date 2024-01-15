from django.urls import path, include

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.home, name="home"),
    path("user_login/",views.user_login, name="user_login"),
    path('utente/<int:id>/', views.UtenteView.as_view(), name='utente'),
    path('medico/<int:id>/', views.MedicoView.as_view(), name='medico'),
    path('familiar/<int:id>/', views.FamiliarView.as_view(), name='familiar'),
    path('auxiliar/<int:id>/', views.AuxiliarView.as_view(), name='auxiliar'),
    path('logout/', views.logout_view, name='logout'),
]