"""
URL configuration for scope_flow_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from scope_flow.views import (home_page,
                              WorkerListView,
                              TaskListView,
                              TaskUpdateView,
                              TaskDeleteView,
                              TaskCreateView,
                              WorkerDetailView, WorkerUpdateView, WorkerDeleteView)

urlpatterns = [
    path("", home_page, name="home-page"),
    path("workers/",
         WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>",
         WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update",
         WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete",
         WorkerDeleteView.as_view(), name="worker-delete"),

    path("tasks/<int:pk>/", TaskListView.as_view(), name="task-list"),
    path('tasks/create/',
         TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/',
         TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/',
         TaskDeleteView.as_view(), name='task-delete'),
]

app_name = "scope_flow"
