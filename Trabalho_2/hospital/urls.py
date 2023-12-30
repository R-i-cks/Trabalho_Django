from django.urls import path

from . import views

app_name = "hospital"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('detail/<int:id>/', views.DetailView.as_view(), name='detail')

]