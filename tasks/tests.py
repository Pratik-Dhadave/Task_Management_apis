from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='Testing task creation',
            due_date='2023-12-31',
            status='Pending',
            owner=self.user
        )

    def test_task_list_create(self):
        url = '/api/tasks/'
        data = {
            'title': 'New Task',
            'description': 'Testing task creation',
            'due_date': '2023-12-31',
            'status': 'Pending',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_detail(self):
        url = f'/api/tasks/{self.task.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_task_update(self):
        url = f'/api/tasks/{self.task.id}/'
        data = {'title': 'Updated Task'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete(self):
        url = f'/api/tasks/{self.task.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
