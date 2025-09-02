from scope_flow.models import Worker

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assignees",
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Describe your task..."
        }),
        label="Description"
    )

    deadline = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        }),
        label="Deadline"
    )

    class Meta:
        model = Task
        fields = ["name", "description",
                  "deadline", "priority",
                  "task_type", "assignees"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Task name"
            }),
            "priority": forms.Select(attrs={
                "class": "form-select"
            }),
            "task_type": forms.Select(attrs={
                "class": "form-select"
            }),
        }
        labels = {
            "name": "Name",
            "priority": "Priority",
            "task_type": "Task type"
        }


class WorkerCreateForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$')
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Worker
        fields = ["username",
                  "email", "first_name",
                  "last_name", "password",
                  "password_confirm", "position"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Паролі не збігаються.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class WorkerUpdateForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$')
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(),
                                       required=False)

    class Meta:
        model = Worker
        fields = ["username", "email", "first_name", "last_name", "position"]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password or password_confirm:
            if password != password_confirm:
                self.add_error("password_confirm", "Passwords don't match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user
