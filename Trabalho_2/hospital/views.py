from django.views import generic
from django.utils import timezone
from .models import Utente, Medico, Medicamento, Consulta
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

class IndexView(generic.ListView):    # Aqui podemos listar as opções de consulta , utente, medico, medicamento, consulta
    template_name = "hospital/index.html"
    context_object_name = "lista_consultas"
    def get_queryset(self):

        return Consulta.objects.all()

class DetailView(generic.DetailView):
    model = Consulta
    template_name = "hospital/detail.html"
    context_object_name = "obj_consulta"
    pk_url_kwarg = 'id'


class UtenteView(generic.DetailView):
    model = Utente
    template_name = "hospital/utente.html"


class MedicoView(generic.DetailView):
    model = Medico
    template_name = "hospital/medico.html"



