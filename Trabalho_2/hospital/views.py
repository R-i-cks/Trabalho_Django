from django.contrib import messages
from django.views import generic
from django.utils import timezone
from .models import Utente, Medico, Medicamento, Consulta
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie



def home(request):
    return render(request,"hospital/login.html")

@ensure_csrf_cookie
def login(request):

    if request.method == "POST" :
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            return render(request, "hospital/index.html")
        else:
            messages.error(request, "Credenciais não reconhecidas")


    return render(request,"hospital/home.html")


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
    model = Consulta
    template_name = "hospital/utente.html"
    context_object_name = "consulta_utente"
    pk_url_kwarg = 'id'

class MedicoView(generic.DetailView):
    model = Consulta
    template_name = "hospital/medico.html"
    context_object_name = "consulta_medico"
    pk_url_kwarg = 'id'


