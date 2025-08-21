from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from scope_flow.models import Task, Worker


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all().filter(),
        widget=forms.CheckboxSelectMultiple,

        required=False)
    description = forms.Textarea()
    deadline = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                               widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = '__all__'


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
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False)

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