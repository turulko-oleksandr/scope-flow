from django.contrib import admin

from scope_flow.models import TaskType, Worker, Task, Position

# Register your models here.
admin.site.register(Worker)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Position)
