from django.test import TestCase
from .models import Machines, ProductionLog
from .services import calculate_oee
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

class OeeCalculationTest(TestCase):
    def setUp(self):
        self.machine = Machines.objects.create(machine_name="Test Machine", machine_serial_no="1234")
        start_time = timezone.now()
        for i in range(5):
            ProductionLog.objects.create(
                cycle_no=f'CN00{i}',
                unique_id=f'UID00{i}',
                material_name='Material A',
                machine=self.machine,
                start_time=start_time,
                end_time=start_time + timedelta(minutes=5),
                duration=5/60
            )
            start_time += timedelta(minutes=5)

    def test_calculate_oee(self):
        logs = ProductionLog.objects.all()
        oee_data = calculate_oee(logs)
        self.assertAlmostEqual(oee_data['availability'], 100)
        self.assertAlmostEqual(oee_data['performance'], 100)
        self.assertAlmostEqual(oee_data['quality'], 100)
        self.assertAlmostEqual(oee_data['oee'], 100)

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machines.objects.create(machine_name="Test Machine", machine_serial_no="1234")

    def test_create_machine(self):
        response = self.client.post('/api/machines/', {'machine_name': 'New Machine', 'machine_serial_no': '5678'})
        self.assertEqual(response.status_code, 201)

    def test_get_oee(self):
        response = self.client.get('/api/oee/')
        self.assertEqual(response.status_code, 200)