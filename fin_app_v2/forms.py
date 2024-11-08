# from django import forms
# from django.contrib.auth.models import User
# from django.forms import inlineformset_factory
#
# from .models import Job, Task
#
# # Job form to create a job (without assigning developers)
# class JobForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ['title', 'client_email', 'client_password']  # Only job details
#
# # Task form to assign developers by email during task creation
# # class TaskForm(forms.ModelForm):
# #     assigned_users = forms.ModelMultipleChoiceField(
# #         queryset=User.objects.filter(is_staff=True),  # Filter for authorized developers
# #         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
# #         label="Assign Developers (by Email)"
# #     )
# #
# #     class Meta:
# #         model = Task
# #         fields = ['title', 'assigned_users', 'description']  # Task details and developers
# #
# #     # Overriding the label to display user emails instead of usernames
# #     def __init__(self, *args, **kwargs):
# #         super(TaskForm, self).__init__(*args, **kwargs)
# #         self.fields['assigned_users'].queryset = User.objects.filter(is_staff=True)
# #         self.fields['assigned_users'].label_from_instance = lambda obj: f"{obj.email}"  # Show email in the dropdown
#
#
# from django import forms
# from .models import Task
# from django.contrib.auth.models import User
#
#
# class TaskForm(forms.ModelForm):
#     assigned_users = forms.ModelMultipleChoiceField(
#         queryset=User.objects.filter(is_staff=True),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
#         label="Assign Developers (by Email)"
#     )
#     deadline = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'}),  # Input for selecting a date
#         required=False,
#         label="Deadline"
#     )
#
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'assigned_users', 'task_percentage', 'progress', 'deadline']
#
#     def __init__(self, *args, **kwargs):
#         super(TaskForm, self).__init__(*args, **kwargs)
#         self.fields['assigned_users'].queryset = User.objects.filter(is_staff=True)
#         self.fields['assigned_users'].label_from_instance = lambda obj: f"{obj.email}"  # Show email instead of username
#
#
# # Inline formset for multiple tasks
# TaskFormSet = forms.inlineformset_factory(Job, Task, form=TaskForm, extra=1)
#
#
# # Client login form definition
# class ClientLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)


#version 2


from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Job, Task

# Job form to create a job (with over_all_income field)
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'client_email', 'client_password', 'over_all_income']  # Added 'over_all_income'




from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Task, Job

class TaskForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Assign Developers (by Email)"
    )
    deadline = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=False,
        label="Deadline"
    )
    hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Hours",
        min_value=1  # Ensure the hours are positive
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_users', 'hours', 'deadline', 'money_for_task']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Display emails of staff users in assigned_users field
        self.fields['assigned_users'].queryset = User.objects.filter(is_staff=True)
        self.fields['assigned_users'].label_from_instance = lambda obj: f"{obj.email}"

# Inline formset for creating multiple Task forms associated with a Job
TaskFormSet = inlineformset_factory(Job, Task, form=TaskForm, extra=1)

# Client login form definition
class ClientLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
