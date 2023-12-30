from rest_framework import serializers
from hospital.models import Utente, Medico, Medicamento, Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'   # pretende-se serializar todos os elementos
