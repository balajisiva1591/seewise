from django.urls import path
from .views import MachinesListCreate, ProductionLogListCreate, oee_data

urlpatterns = [
    path('machines/', MachinesListCreate.as_view(), name='machines list create'),
    path('production_logs/', ProductionLogListCreate.as_view(), name='production log list create'),
    path('oee/', oee_data, name='oee-data'),
]
