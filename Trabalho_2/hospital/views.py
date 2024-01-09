from django.contrib import messages
from django.views import generic
from django.utils import timezone
from .models import Utente, Medico, Medicamento, Consulta
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie



def home(request):
    return render(request,"hospital/home.html")

@ensure_csrf_cookie
def user_login(request):

    if request.method == "POST" :
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            user_group = user.groups.first()
            if user_group.name == "Utente":
                utente_id = Utente.objects.get(nome=username).id
                print(utente_id)
                return redirect("hospital:utente", id=utente_id)
            elif user_group.name == "Medico":
                medico_id = Medico.objects.get(nome=username).id
                return redirect("hospital:medico", id=medico_id)

        else:
            messages.error(request, "Credenciais não reconhecidas")
            return redirect("hospital:home")

    return render(request,"hospital/login.html")

# @login_required para o que for preciso login
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


