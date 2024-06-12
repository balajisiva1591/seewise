from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import Machines, ProductionLog
from .serializers import MachinesSerializer, ProductionLogSerializer
from .services import calculate_oee
import datetime

class MachinesListCreate(generics.ListCreateAPIView):
    queryset = Machines.objects.all()
    serializer_class = MachinesSerializer

class ProductionLogListCreate(generics.ListCreateAPIView):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

@api_view(['GET'])
def oee_data(request):
    print ("bbbbbb",request)
    machine_id = request.query_params.get('machine')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    logs = ProductionLog.objects.all()
    if machine_id:
        logs = logs.filter(machine__id=machine_id)
    if start_date:
        logs = logs.filter(start_time__gte=start_date)
    if end_date:
        logs = logs.filter(end_time__lte=end_date)

    oee = calculate_oee(logs) 
    print(oee)
    return Response(oee)
