from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from scope_flow.models import Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all().filter(),
        widget=forms.CheckboxSelectMultiple,

        required=False)
    description = forms.Textarea()
    deadline = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = '__all__'
