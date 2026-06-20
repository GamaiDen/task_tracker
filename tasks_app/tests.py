from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from employees.models import Employee
from .models import Task


class TaskTests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(full_name='Иванов Иван', position='Разработчик')
        self.parent_task = Task.objects.create(
            name='Родительская задача', executor=self.employee,
            deadline='2026-07-01', status='in_progress'
        )
        self.child_task = Task.objects.create(
            name='Зависимая задача', parent_task=self.parent_task,
            deadline='2026-07-10', status='new'
        )
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', kwargs={'pk': self.parent_task.pk})

    def test_list_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_task(self):
        data = {'name': 'Новая задача', 'deadline': '2026-08-01', 'status': 'new'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_update_task(self):
        data = {'name': 'Обновлённая', 'deadline': '2026-07-01', 'status': 'in_progress'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_important_tasks(self):
        response = self.client.get(reverse('task-important'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Зависимая задача
        self.assertEqual(response.data[0]['task'], 'Зависимая задача')
