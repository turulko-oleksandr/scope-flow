from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView

from .forms import TaskForm, WorkerCreateForm
from scope_flow.models import Worker, Task


def home_page(request):
    return render(request, "base.html")


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("scope_flow:home-page")

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.object
        login(self.request, user)

        return response


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "worker/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "worker/worker_details.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    queryset = (Task.objects.all()
                .prefetch_related('assignees')
                .order_by('deadline'))
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('scope_flow:task-list')


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/task_form.html"
    success_url = reverse_lazy('scope_flow:task-list')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task/task_confirm_delete.html"
    success_url = reverse_lazy('scope_flow:task-list')
