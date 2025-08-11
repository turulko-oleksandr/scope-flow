from django.contrib.auth.models import User, AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType,on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker)

    def __str__(self):
        return self.name
