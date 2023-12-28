from django.views import generic
from django.utils import timezone
from .models import Utente, Medico, Medicamento, Consulta


class IndexView(generic.ListView):    # Aqui podemos listar as opções de consulta , utente, medico, medicamento, consulta
    template_name = "hospital/index.html"


class UtenteView(generic.DetailView):
    model = Utente
    template_name = "hospital/utente.html"


class MedicoView(generic.DetailView):
    model = Medico
    template_name = "hospital/medico.html"


class MedicamentoView(generic.DetailView):
    model = Medicamento
    template_name = "hospital/medicamento.html"


class ConsultaView(generic.DetailView):
    model = Consulta
    template_name = "polls/consulta.html"


