from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView

from .forms import TaskForm, WorkerCreateForm, WorkerUpdateForm
from scope_flow.models import Worker, Task
from django.views import View
from django.shortcuts import get_object_or_404, redirect


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
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "worker/worker_details.html"


class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You are not the owner of this worker.")
        return obj


class WorkerUpdateView(LoginRequiredMixin, OwnerRequiredMixin, generic.UpdateView):
    model = Worker
    template_name = "worker/worker_form.html"
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("scope_flow:home-page")


class WorkerDeleteView(LoginRequiredMixin, OwnerRequiredMixin, generic.DeleteView):
    model = Worker
    context_object_name = "worker"
    template_name = "worker/worker_confirm_delete.html"
    success_url = reverse_lazy("scope_flow:home-page")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5
    def get_queryset(self):
        worker_id = self.kwargs.get("pk")
        return (Task.objects.
                prefetch_related("assignees").
                filter(assignees__id=worker_id))


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


class TaskSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = True
        task.save()
        return redirect('scope_flow:task-list', pk=request.user.pk)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task/task_confirm_delete.html"
    success_url = reverse_lazy('scope_flow:task-list')
