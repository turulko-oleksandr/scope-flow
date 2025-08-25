from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from scope_flow.models import Task, TaskType, Position, Worker

User = get_user_model()


class WorkerViewsTests(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.position = Position.objects.create(name="Developer")

        self.user = User.objects.create_user(
            username="testuser",
            password=self.password,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            position=self.position
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="pass12345",
            position=self.position
        )
        self.client.login(username="testuser", password=self.password)

    def test_worker_list_view_authenticated(self):
        response = self.client.get(reverse("scope_flow:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "Developer")

    def test_worker_detail_view(self):
        response = self.client.get(
            reverse("scope_flow:worker-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertContains(response, "Developer")

    def test_worker_update_view_owner_only(self):
        other_user = Worker.objects.create_user(username="other", password="pass")
        self.client.login(username="taskuser", password="password")
        response = self.client.get(reverse("scope_flow:worker-update", kwargs={"pk": other_user.pk}))
        self.assertEqual(response.status_code, 403)  # перевіряємо саме статус


class TaskViewsTests(TestCase):
    def setUp(self):
        self.password = "taskpass123"
        self.position = Position.objects.create(name="QA")
        self.task_type = TaskType.objects.create(name="Bugfix")

        self.user = User.objects.create_user(
            username="taskuser",
            password=self.password,
            position=self.position
        )
        self.client.login(username="taskuser", password=self.password)

        self.task = Task.objects.create(
            name="Fix login bug",
            description="User cannot log in",
            deadline=timezone.now().date(),
            priority="High",
            task_type=self.task_type,
            author=self.user,
        )
        self.task.assignees.add(self.user)

    def test_task_list_view_only_user_tasks(self):
        response = self.client.get(reverse("scope_flow:task-list", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login bug")

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("scope_flow:task-detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fix login bug")
        self.assertContains(response, "User cannot log in")
        self.assertContains(response, "Bugfix")

    def test_task_create_view(self):
        response = self.client.post(
            reverse("scope_flow:task-create"),
            {
                "name": "Write tests",
                "description": "Add unit tests",
                "deadline": timezone.now().date(),
                "priority": "Medium",
                "task_type": self.task_type.pk,
                "author": self.user.pk,
                "assignees": [self.user.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Write tests").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("scope_flow:task-update", kwargs={"pk": self.task.pk}),
            {
                "name": "Fix login bug - updated",
                "description": "Fixed properly",
                "deadline": timezone.now().date(),
                "priority": "Urgent",
                "task_type": self.task_type.pk,
                "author": self.user.pk,
                "assignees": [self.user.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Fix login bug - updated")
        self.assertEqual(self.task.priority, "Urgent")

    def test_task_submit_view_marks_completed(self):
        response = self.client.post(reverse("scope_flow:task-submit", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_task_delete_view(self):
        response = self.client.post(reverse("scope_flow:task-delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
