from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.db.models.functions import Coalesce, NullIf

from .forms import TaskForm
from .models import Task, TaskType, Position, Worker
from scope_flow.models import Worker, Task


def home_page(request):
    return render(request, "base.html")

class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "worker/worker_list.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    queryset = Task.objects.all().prefetch_related('assignees').order_by('deadline')
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task/task_delete_confirm_form.html"
