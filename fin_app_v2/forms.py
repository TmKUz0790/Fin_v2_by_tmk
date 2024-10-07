from django import forms
from django.forms import inlineformset_factory
from .models import Job, Task

# Job form to create a job and assign a client
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'client', 'assigned_users']

# Task form to create tasks and assign developers
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_users', 'description']

# Formset for handling multiple Task forms
TaskFormSet = inlineformset_factory(Job, Task, form=TaskForm, extra=1)
