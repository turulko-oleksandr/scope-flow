from django.shortcuts import render
from django.views import generic

from scope_flow.models import Worker, Task


def home_page(request):
    return render(request,"base.html")

class WorkerListView(generic.ListView):
    model = Worker
    template_name = "worker/worker_list.html"


from django.views.generic import ListView
from django.db.models.functions import Coalesce, NullIf
from .models import Task, TaskType, Position, Worker


class TaskListView(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all().order_by(
            Coalesce(
                NullIf('priority', 'Urgent'),
                NullIf('priority', 'High'),
                NullIf('priority', 'Medium'),
                NullIf('priority', 'Low')
            ).desc()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        priorities = [
            ("Urgent", "Urgent"),
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low"),
        ]

        grouped_tasks = {}
        for priority_value, priority_label in priorities:
            tasks = Task.objects.filter(priority=priority_value).order_by('deadline')
            grouped_tasks[priority_label] = tasks

        context['grouped_tasks'] = grouped_tasks
        return context


class TaskUpdateView(generic.UpdateView):
    model = Task


class TaskDeleteView(generic.DeleteView):
    model = Task
