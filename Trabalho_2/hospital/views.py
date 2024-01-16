from django.contrib import messages
from django.db.models import Count
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import *
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, "hospital/home.html")


@ensure_csrf_cookie
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            preferred_groups = [
                "Utente",
                "Medico",
                "Familiar",
                "Auxiliar",
                "Enfermeiro",
            ]

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
                            return redirect("hospital:auxiliar", id=auxiliar_id)

                        elif group_name == "Enfermeiro":
                            enfermeiro_id = Enfermeiro.objects.get(nome=username).id
                            return redirect("hospital:enfermeiro", id=enfermeiro_id)

                except Group.DoesNotExist:
                    messages.error(request, "Credenciais inválidas")
                    return redirect("hospital:user_login")

    return render(request, "hospital/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return render(request, "hospital/logout.html")


class IndexView(generic.ListView):
    template_name = "hospital/index.html"
    context_object_name = "lista_consultas"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Consulta.objects.all()


class ListaConsultas(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "hospital/lista_consultas.html"
    context_object_name = "lista_consultas"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Consulta.objects.all()


class ListaUtentes(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "hospital/index.html"
    context_object_name = "lista_utentes"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Utentes.objects.all()


class UtenteView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Consulta
    template_name = "hospital/utente.html"
    context_object_name = "consultas_utente"
    pk_url_kwarg = "id"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        utente = self.get_object()
        if grupos_utilizador.filter(
            name="Profissional"
        ).exists():  # Se True acede cc nao
            return True
        elif grupos_utilizador.filter(name="Familiar").exists():
            familiar = get_object_or_404(Familiar, nome=self.request.user.username)
            return familiar.utente.filter(nome=utente.nome).exists()
        elif grupos_utilizador.filter(name="Utente").exists():
            return utente.nome == self.request.user.username
        else:
            return False

    def get_object(self, queryset=None):
        return get_object_or_404(Utente, id=self.kwargs["id"])

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utente = self.object
        consultas_utente = Consulta.objects.filter(utente=utente)
        context["consultas_utente"] = consultas_utente
        return context


class MedicoView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Consulta
    template_name = "hospital/medico.html"
    context_object_name = "consultas_medico"
    pk_url_kwarg = "id"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        medico = self.get_object()
        if grupos_utilizador.filter(name="Medico").exists():
            return medico.nome == self.request.user.username
        else:
            return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_object(self, queryset=None):
        return get_object_or_404(Medico, id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medico = self.object
        consultas_medico = Consulta.objects.filter(medico=medico)
        context["consultas_medico"] = consultas_medico
        return context


class EnfermeiroView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Medicoes
    template_name = "hospital/enfermeiro.html"
    context_object_name = "consultas_enfermeiro"
    login_url = "hospital:user_login"
    pk_url_kwarg = "id"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        enfermeiro = self.get_object()
        return grupos_utilizador.filter(name="Enfermeiro").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_object(self, queryset=None):
        return get_object_or_404(Enfermeiro, id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enfermeiro = self.get_object()
        consultas_enfermeiro = Medicoes.objects.filter(enfermeiro=enfermeiro)
        context["consultas_enfermeiro"] = consultas_enfermeiro
        return context


class FamiliarView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Consulta
    template_name = "hospital/index.html"
    context_object_name = "utentes_familiares"
    pk_url_kwarg = "id"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        familiar = self.get_object()
        if grupos_utilizador.filter(name="Familiar").exists():
            return familiar.nome == self.request.user.username
        else:
            return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_object(self, queryset=None):
        return get_object_or_404(Familiar, id=self.kwargs["id"])

    def get_queryset(self):
        familiar = self.get_object()
        lista_utentes = familiar.utente.all()
        return lista_utentes


class AuxiliarView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "hospital/index.html"
    context_object_name = "dados"
    login_url = "hospital:user_login"

    def test_func(
        self,
    ):  # Como se trata de uma pag igual para todos os auxiliares, e este é o user com mais permisssões, so os membros deste grupo podem aceder
        return self.request.user.groups.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Turn around, nothing to see here")

    def get_queryset(self):
        return Consulta.objects.all()


class MedicamentoView(LoginRequiredMixin, generic.DetailView):
    model = Medicamento
    template_name = "hospital/medicamento.html"
    context_object_name = "medicamento"
    pk_url_kwarg = "id"
    login_url = "hospital:user_login"

    def get_object(self, queryset=None):
        return get_object_or_404(Medicamento, id=self.kwargs["id"])


class ListaUtentesView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Utente
    template_name = "hospital/index.html"
    context_object_name = "utentes"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Profissional").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Utente.objects.all()


class ListaConsultasView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Consulta
    template_name = "hospital/index.html"
    context_object_name = "consultas"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Profissional").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Consulta.objects.all()


class ListaMedicosView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Medico
    template_name = "hospital/index.html"
    context_object_name = "medicos"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Medico.objects.all()


class ListaFamiliaresView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Familiar
    template_name = "hospital/index.html"
    context_object_name = "familiares"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Familiar.objects.all()


class ListaEnfermeirosView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Enfermeiro
    template_name = "hospital/index.html"
    context_object_name = "enfermeiros"
    login_url = "hospital:user_login"

    def test_func(self):
        grupos_utilizador = self.request.user.groups
        return grupos_utilizador.filter(name="Auxiliar").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Where the hell you think you're going uh?")

    def get_queryset(self):
        return Enfermeiro.objects.all()


class ListaMedicamentosView(LoginRequiredMixin, generic.ListView):
    model = Medicamento
    template_name = "hospital/index.html"
    context_object_name = "medicamentos"
    login_url = "hospital:user_login"

    def get_queryset(self):
        return Medicamento.objects.all()
