from django.contrib import admin
from .models import Consulta,  Utente, Medico, Medicamento

admin.site.register(Utente)
admin.site.register(Medico)
admin.site.register(Medicamento)
admin.site.register(Consulta)

