from django.contrib import messages
from django.db.models import Count
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import *
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

def home(request):
    return render(request,"hospital/home.html")


@ensure_csrf_cookie
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            preferred_groups = ["Utente", "Medico", "Familiar", "Auxiliar"]

            for group_name in preferred_groups:
                try:
                    group = Group.objects.get(name=group_name)
                    if group in user.groups.all():
                        if group_name == "Utente":
                            utente_id = Utente.objects.get(nome=username).id
                            return redirect("hospital:utente", id=utente_id)

                        elif group_name == "Medico":
                            medico_id = Medico.objects.get(nome=username).id
                            return redirect("hospital:medico", id=medico_id)

                        elif group_name == "Familiar":
                            familiar_id = Familiar.objects.get(nome=username).id
                            return redirect("hospital:familiar", id=familiar_id)

                        elif group_name == "Auxiliar":
                            auxiliar_id = Auxiliar.objects.get(nome=username).id
                            return redirect("hospital:index_auxiliar", id=auxiliar_id)

                except Group.DoesNotExist:
                    messages.error(request, "Credenciais inválidas")
                    return redirect("hospital:user_login")

    return render(request,"hospital/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return render(request,"hospital/logout.html")

class IndexView(generic.ListView):    # Aqui podemos listar as opções de consulta , utente, medico, medicamento, consulta
    template_name = "hospital/index.html"
    context_object_name = "lista_consultas"
    def get_queryset(self):
        return Consulta.objects.all()

class ListaConsultas(generic.ListView):    # Aqui podemos listar as opções de consulta , utente, medico, medicamento, consulta
    template_name = "hospital/lista_consultas.html"
    context_object_name = "lista_consultas"
    def get_queryset(self):
        return Consulta.objects.all()
    
class IndexAuxiliarView(generic.ListView):
    template_name = 'hospital/index_auxiliar.html'
    context_object_name = "index_auxiliar"
    pk_url_kwarg = 'id'
    def get(self, request, id):
        return render(request, self.template_name, {'id': id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultas_todas = Consulta.objects.all()
        context['consultas_todas'] = consultas_todas
        return context

class UtenteView(LoginRequiredMixin,generic.DetailView):
    model = Consulta
    template_name = "hospital/utente.html"
    context_object_name = "consultas_utente"
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        return get_object_or_404(Utente, id=self.kwargs['id'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utente = self.object
        consultas_utente = Consulta.objects.filter(utente=utente)
        context['consultas_utente'] = consultas_utente
        return context

class MedicoView(LoginRequiredMixin,generic.DetailView):
    model = Consulta
    template_name = "hospital/medico.html"
    context_object_name = "consultas_medico"
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        return get_object_or_404(Medico, id=self.kwargs['id'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medico = self.object
        consultas_medico = Consulta.objects.filter(medico=medico)
        context['consultas_medico'] = consultas_medico
        return context

class FamiliarView(LoginRequiredMixin, generic.ListView):
    model = Consulta
    template_name = "hospital/index.html"
    context_object_name = "utentes_familiares"
    pk_url_kwarg = 'id'
    def get_object(self, queryset=None):
        return get_object_or_404(Familiar, id=self.kwargs['id'])
    def get_queryset(self):
        familiar = self.get_object()
        lista_utentes = familiar.utente.all()
        return lista_utentes

class AuxiliarView(LoginRequiredMixin, generic.ListView):
    model = Consulta
    template_name = "hospital/auxiliar.html"
    context_object_name = "consultas_todas"

    def get_queryset(self):
        return Consulta.objects.all()