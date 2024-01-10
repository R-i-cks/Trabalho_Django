from rest_framework.response import Response  # pega dados em py serializados e renderiza em json
from rest_framework.decorators import  api_view
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth.models import User
from hospital.models import Consulta
from .serializers import ConsultaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UtenteView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),  # None
        }
        return Response(content)

class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    # Deste modo apenas os admin terão acesso à lista de utilizadores

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
        #lista de users




@api_view(['GET']) # métodos permitidos
# POST, PUT DELETE  podem ser adicionados
def getData(request):
    consultas = Consulta.objects.all()  # Pegar em todos os dados
    serializer = ConsultaSerializer(consultas, many=True) #Serializar antes de retornar
    # O many indica que vamos serializar mais do que um objeto
    return Response(serializer.data)
# Precisamos de um end point para ver o output

@api_view(['POST'])
def addConsulta(request):
    serializer = ConsultaSerializer(data=request.data)
    # Vamos serializar os dados recebidos no pedido
    #Para ver se é válido
    if serializer.is_valid():
        serializer.save() # Cria uma nova consulta na BD
    return Response(serializer.data)

