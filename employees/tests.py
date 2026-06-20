from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee


class EmployeeTests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            full_name='Иванов Иван', position='Разработчик'
        )
        self.list_url = reverse('employee-list')
        self.detail_url = reverse('employee-detail', kwargs={'pk': self.employee.pk})

    def test_list_employees(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_employee(self):
        data = {'full_name': 'Петров Пётр', 'position': 'Менеджер'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_update_employee(self):
        data = {'full_name': 'Иванов Иван Updated', 'position': 'Сеньор'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.position, 'Сеньор')

    def test_delete_employee(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_busy_employees(self):
        response = self.client.get(reverse('employee-busy'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
