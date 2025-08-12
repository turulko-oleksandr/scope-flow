from django.shortcuts import render
from django.views import generic

from scope_flow.models import Worker, Task


# Create your views here.
def home_page(request):
    return render(request,"base.html")

class WorkerListView(generic.ListView):
    model = Worker
    template_name = "worker/worker_list.html"


class TaskListView(generic.ListView):
    model = Task
    template_name = "task/task_list.html"
