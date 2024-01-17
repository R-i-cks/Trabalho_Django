from django.contrib import messages
from django.views import generic
from django.views.decorators.http import require_POST


from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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


def add_consulta(request):
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = ConsultaForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_utente(request):
    if request.method == "POST":
        form = UtenteForm(request.POST)
        if form.is_valid():
            grupo_utentes, _ = Group.objects.get_or_create(name="Utente")
            form.save()
            username = form.cleaned_data["nome"]
            password = "password"
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.groups.add(grupo_utentes)
            user.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = UtenteForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


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


def add_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            grupo_medicos, _ = Group.objects.get_or_create(name="Medico")
            grupo_profissionais, _ = Group.objects.get_or_create(name="Profissional")
            form.save()
            username = form.cleaned_data["nome"]
            password = "password"
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.groups.add(grupo_medicos, grupo_profissionais)
            user.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = MedicoForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_enfermeiro(request):
    if request.method == "POST":
        form = EnfermeiroForm(request.POST)
        if form.is_valid():
            grupo_enfermeiros, _ = Group.objects.get_or_create(name="Enfermeiro")
            grupo_profissionais, _ = Group.objects.get_or_create(name="Profissional")
            form.save()
            username = form.cleaned_data["nome"]
            password = "password"
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.groups.add(grupo_enfermeiros, grupo_profissionais)
            user.save()
            form.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = EnfermeiroForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_medicamento(request):
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = MedicamentoForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_familiar(request):
    if request.method == "POST":
        form = FamiliarForm(request.POST)
        if form.is_valid():
            grupo_familiares, _ = Group.objects.get_or_create(name="Familiar")
            username = form.cleaned_data["nome"]
            password = "password"
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.groups.add(grupo_familiares)
            form.save()
            user.save()
            return redirect("hospital:auxiliar", id=1)
    else:
        form = FamiliarForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_prescricao(request, consulta_id, medico_id, utente_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    utente = get_object_or_404(Utente, pk=utente_id)
    consulta = get_object_or_404(Consulta, pk=consulta_id)

    if request.method == "POST":
        form = PrescricoesForm(request.POST)
        if form.is_valid():
            prescricao = form.save(commit=False)
            prescricao.utente = utente
            prescricao.medico = medico
            prescricao.save()
            consulta.prescricoes.add(prescricao)
            consulta.save()
            return redirect("hospital:medico", id=medico.id)
    else:
        form = PrescricoesForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_medicao(request, consulta_id, medico_id, utente_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    utente = get_object_or_404(Utente, pk=utente_id)
    consulta = get_object_or_404(Consulta, pk=consulta_id)

    if request.method == "POST":
        form = MedicoesForm(request.POST)
        if form.is_valid():
            medicao = form.save(commit=False)
            medicao.utente = utente
            if prof == "medico":
                medicao.medico = profissional
            else:
                medicao.enfermeiro = profissional
            medicao.save()
            consulta.medicoes.add(medicao)
            consulta.save()
            if prof == "medico":
                return redirect("hospital:medico", id=profissional.id)
            else:
                return redirect("hospital:enfermeiro", id=profissional.id)
    else:
        form = MedicoesForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


def add_exame(request, consulta_id, prof, profissional_id, utente_id):
    if prof == "medico":
        profissional = get_object_or_404(Medico, pk=profissional_id)
    else:
        profissional = get_object_or_404(Enfermeiro, pk=profissional_id)
    utente = get_object_or_404(Utente, pk=utente_id)
    consulta = get_object_or_404(Consulta, pk=consulta_id)

    if request.method == "POST":
        form = ExamesForm(request.POST)
        if form.is_valid():
            exame = form.save(commit=False)
            exame.utente = utente
            if prof == "medico":
                exame.medico = profissional
            else:
                exame.enfermeiro = profissional
            exame.save()
            consulta.exames.add(exame)
            consulta.save()
            if prof == "medico":
                return redirect("hospital:medico", id=profissional.id)
            else:
                return redirect("hospital:enfermeiro", id=profissional.id)
    else:
        form = ExamesForm()
    return render(request, "hospital/add_consulta.html", {"form": form})


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
        context["enfermeiro"] = enfermeiro
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        familiar = self.get_object()
        context["familiar"] = familiar
        return context


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


class EstatisticaView(generic.ListView):
    template_name = "stats.html"

    login_url = "hospital:user_login"

    def get_context_data(self, **kwargs):
        context = {}
        pessoas = Utente.objects.all()
        homens = pessoas.filter(genero="M")
        mulheres = pessoas.filter(genero="F")

        soma = 0
        i = 0
        for pessoa in pessoas:
            i += 1
            soma += pessoa.idade()
        media = soma / i

        prescricoes = Prescricoes.objects.all()
        presc_med = {}

        for prescricao in prescricoes:
            if prescricao.medicamento.nome in presc_med.keys():
                presc_med[prescricao.medicamento.nome] += 1
            else:
                presc_med[prescricao.medicamento.nome] = 1

        maior = -10
        chave1 = ""
        for elem in presc_med.keys():
            if presc_med[elem] > maior:
                maior = presc_med[elem]
                chave1 = elem  # medicamento mais prescrito

        p_medicos = {}

        for prescricao in prescricoes:
            if prescricao.medico in p_medicos.keys():
                p_medicos[prescricao.medico] += 1
            else:
                p_medicos[prescricao.medico] = 1

        maior = -10
        chave2 = ""
        for elem in p_medicos.keys():
            if p_medicos[elem] > maior:
                maior = p_medicos[elem]
                chave2 = elem  # medico c +  prescricoes

        exames = Exame.objects.all()

        conta_exames = {}

        for exame in exames:
            if exame.nome_exame in conta_exames.keys():
                conta_exames[exame.nome_exame] += 1
            else:
                conta_exames[exame.nome_exame] = 1

        maior = -10
        chave3 = ""
        for elem in conta_exames.keys():
            if conta_exames[elem] > maior:
                maior = conta_exames[elem]
                chave3 = elem  # exame mais prescrito

        context["total_users"] = pessoas
        context["n_homens"] = homens
        context["n_mulheres"] = mulheres
        context["idade_media"] = media
        context["medicamento_mais_p"] = chave1
        context["medico_mais_p"] = chave2
        context["exame_mais_p"] = chave3

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
