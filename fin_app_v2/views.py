# #version 2
# from django.contrib.auth.hashers import make_password, check_password
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from .forms import JobForm, TaskFormSet, ClientLoginForm
# from .models import Job, Task
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
#
#
# # View to create a job (with overall income field)
# # def create_job(request):
# #     if request.method == 'POST':
# #         job_form = JobForm(request.POST)
# #         if job_form.is_valid():
# #             job = job_form.save(commit=False)
# #             # Hash the client's password before saving
# #             job.client_password = make_password(job_form.cleaned_data['client_password'])
# #             job.save()
# #             return redirect('task_create', job_id=job.id)  # Redirect to task creation
# #     else:
# #         job_form = JobForm()
# #
# #     return render(request, 'create_job.html', {'job_form': job_form})
#
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
#
# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         try:
#             # Fetch the user by email
#             user = User.objects.get(email=email)
#             # Authenticate using the username (Django default) and password
#             if user.check_password(password):
#                 # Log the user in and redirect to the create job view if email is correct
#                 login(request, user)
#                 return redirect('create_job')
#             else:
#                 messages.error(request, "Invalid password")
#         except User.DoesNotExist:
#             messages.error(request, "User with this email does not exist")
#     return render(request, 'login.html')
# @login_required
# def create_job(request):
#     # Check if the logged-in user has the allowed email
#     if request.user.email != 'admin_tmk@gmail.com':
#         # Return a 403 Forbidden response if the user is not authorized
#         return HttpResponseForbidden("You are not authorized to access this page.")
#
#     if request.method == 'POST':
#         job_form = JobForm(request.POST)
#         if job_form.is_valid():
#             job = job_form.save(commit=False)
#             # Hash the client's password before saving
#             job.client_password = make_password(job_form.cleaned_data['client_password'])
#             job.save()
#             return redirect('task_create', job_id=job.id)  # Redirect to task creation
#     else:
#         job_form = JobForm()
#
#     return render(request, 'create_job.html', {'job_form': job_form})
#
#
#
# def create_tasks(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#
#     if request.method == 'POST':
#         task_formset = TaskFormSet(request.POST, instance=job)
#
#         if task_formset.is_valid():
#             # First, calculate the total hours for all tasks
#             total_hours = sum([form.cleaned_data['hours'] for form in task_formset if form.cleaned_data.get('hours')])
#
#             # Now iterate over the formset and calculate the percentage for each task
#             for form in task_formset:
#                 task = form.save(commit=False)
#                 task.task_percentage = (form.cleaned_data['hours'] / total_hours) * 100
#                 task.save()
#
#             return redirect('job_list')  # Redirect to job list after saving tasks
#     else:
#         task_formset = TaskFormSet(instance=job)
#
#     return render(request, 'create_tasks.html', {
#         'task_formset': task_formset,
#         'job': job,
#     })
from datetime import timezone

#
# # View to list jobs
# def job_list(request):
#     jobs = Job.objects.all()
#     return render(request, 'job_list.html', {'jobs': jobs})
#
#
# # View for client login
# def client_login(request):
#     if request.method == 'POST':
#         form = ClientLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#
#             # Find the job associated with this client
#             try:
#                 job = Job.objects.get(client_email=email)
#                 if check_password(password, job.client_password):
#                     # Store job id in session and redirect to progress page
#                     request.session['client_job_id'] = job.id
#                     return redirect('client_progress')
#                 else:
#                     messages.error(request, 'Invalid password')
#             except Job.DoesNotExist:
#                 messages.error(request, 'No job found for this email')
#     else:
#         form = ClientLoginForm()
#
#     return render(request, 'client_login.html', {'form': form})
#
#
# # View to show client progress
# def client_progress(request):
#     job_id = request.session.get('client_job_id')
#     if not job_id:
#         return redirect('client_login')
#
#     job = get_object_or_404(Job, id=job_id)
#     tasks = job.tasks.all()
#
#     return render(request, 'client_progress.html', {'job': job, 'tasks': tasks})
#
#
# # View for developer login and viewing their tasks
# def developer_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         # Authenticate based on email (developers log in using email)
#         try:
#             user = User.objects.get(email=email)
#             if user.check_password(password):
#                 # Log the developer in
#                 login(request, user)
#                 return redirect('developer_tasks')  # Redirect to developer's tasks
#             else:
#                 messages.error(request, 'Invalid password')
#         except User.DoesNotExist:
#             messages.error(request, 'User with this email does not exist')
#     return render(request, 'developer_login.html')
#
#
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Task
#
# @login_required
# def developer_tasks(request):
#     if request.method == 'POST':
#         task_id = request.POST.get('task_id')
#         progress = request.POST.get('progress')
#         feedback = request.POST.get('feedback')
#
#         # Update the task progress and feedback
#         task = get_object_or_404(Task, id=task_id)
#         task.progress = int(progress)
#         task.feedback = feedback
#         task.save()
#
#         # Check if the developer has completed the task (progress = 100%) and handle payment
#         task.check_and_pay_developer()
#
#     # Fetch tasks assigned to the logged-in developer
#     tasks = Task.objects.filter(assigned_users=request.user)
#
#     # Calculate the developer's balance (total money from completed tasks)
#     balance = sum(task.money_for_task for task in tasks if task.paid)
#
#     return render(request, 'developer_tasks.html', {
#         'tasks': tasks,
#         'balance': balance,  # Pass the balance to the template
#     })
#
#
#
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.utils.timezone import now
# from .models import Job, Task, DeductionLog
#
# # Admin Dashboard view
# # def admin_dashboard(request):
# #     today = now().date()
# #
# #     # Get all developers who are staff members
# #     developers = User.objects.filter(is_staff=True)
# #
# #     developer_data = []
# #     for developer in developers:
# #         tasks = Task.objects.filter(assigned_users=developer)
# #         developer_tasks = []
# #
# #         for task in tasks:
# #             if task.deadline:
# #                 # Calculate days remaining until the deadline
# #                 days_until_deadline = (task.deadline - today).days
# #             else:
# #                 days_until_deadline = None  # Handle tasks without deadlines
# #
# #             developer_tasks.append({
# #                 'task': task,
# #                 'days_until_deadline': days_until_deadline
# #             })
# #
# #         # Calculate the current balance for the developer
# #         balance = sum(task.money_for_task for task in tasks if task.paid)
# #
# #         developer_data.append({
# #             'developer': developer,
# #             'tasks': developer_tasks,
# #             'balance': balance
# #         })
# #
# #     # Get all jobs
# #     jobs = Job.objects.all()
# #
# #     # Fetch deduction logs
# #     deduction_logs = DeductionLog.objects.all()
# #
# #     return render(request, 'admin_dashboard.html', {
# #         'developer_data': developer_data,
# #         'jobs': jobs,
# #         'all_deduction_logs': all_deduction_logs,
# #         'today': today
# #     })
# #
# #
# # # View for deducting balance for a developer on a separate page
# # def deduct_balance(request, developer_id):
# #     developer = get_object_or_404(User, id=developer_id)
# #     tasks = Task.objects.filter(assigned_users=developer)
# #
# #     if request.method == 'POST':
# #         deduction_amount = int(request.POST.get('deduction_amount', 0))
# #         current_balance = sum(task.money_for_task for task in tasks if task.paid)
# #
# #         if deduction_amount <= current_balance:
# #             original_deduction_amount = deduction_amount  # Store the original deduction amount for logging
# #
# #             for task in tasks.filter(paid=True):
# #                 if deduction_amount <= 0:
# #                     break
# #                 if task.money_for_task <= deduction_amount:
# #                     deduction_amount -= task.money_for_task
# #                     task.money_for_task = 0
# #                 else:
# #                     task.money_for_task -= deduction_amount
# #                     deduction_amount = 0
# #                 task.save()
# #
# #             # Ensure the deduction amount was valid and create a log entry
# #             DeductionLog.objects.create(
# #                 developer=developer,
# #                 deducted_by=request.user,
# #                 deduction_amount=original_deduction_amount,  # Use the original amount for logging
# #                 deduction_date=now(),  # Log the time of deduction
# #             )
# #
# #             messages.success(request, f"Successfully deducted {original_deduction_amount} USD from {developer.username}'s balance.")
# #         else:
# #             messages.error(request, "Deduction amount exceeds current balance.")
# #         return redirect('admin_dashboard')
# #
# #     # Calculate current balance for the developer
# #     balance = sum(task.money_for_task for task in tasks if task.paid)
# #
# #     return render(request, 'deduct_balance.html', {
# #         'developer': developer,
# #         'balance': balance,
# #     })
# #
# # # Job list view
# # def job_list(request):
# #     jobs = Job.objects.all()
# #     return render(request, 'job_list.html', {'jobs': jobs})
# #
# #
# # # Deduction logs view
# # # def deduction_logs(request):
# # #     deduction_logs = DeductionLog.objects.all()
# # #     return render(request, 'deduction_logs.html', {'deduction_logs': deduction_logs})
# #
# #
# # # Deduction logs view for a specific developer
# # def deduction_logs(request, developer_id):
# #     developer = get_object_or_404(User, id=developer_id)
# #     logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')  # Order by latest
# #
# #     return render(request, 'deduction_logs.html', {
# #         'developer': developer,
# #         'deduction_logs': logs,
# #     })
# #
#
#
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
# from django.utils.timezone import now
# from django.contrib.auth.decorators import login_required
# from .models import DeductionLog, Task, Job
# from django.contrib import messages
#
# # View to display all deduction logs (for the admin)
# @login_required
# def all_deduction_logs(request):
#     logs = DeductionLog.objects.all().order_by('-deduction_date')
#     return render(request, 'all_deduction_logs.html', {'deduction_logs': logs})
#
# # View to display deduction logs for a specific developer
# @login_required
# def deduction_logs(request, developer_id):
#     developer = get_object_or_404(User, id=developer_id)
#     logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')
#     return render(request, 'deduction_logs.html', {
#         'developer': developer,
#         'deduction_logs': logs,
#     })
#
# # Admin Dashboard view
# @login_required
# def admin_dashboard(request):
#     developers = User.objects.filter(is_staff=True)
#     developer_data = []
#
#     for developer in developers:
#         tasks = Task.objects.filter(assigned_users=developer)
#         developer_tasks = [
#             {
#                 'task': task,
#                 'days_until_deadline': (task.deadline - now().date()).days if task.deadline else None
#             }
#             for task in tasks
#         ]
#         balance = sum(task.money_for_task for task in tasks if task.paid)
#         developer_data.append({
#             'developer': developer,
#             'tasks': developer_tasks,
#             'balance': balance
#         })
#
#     return render(request, 'admin_dashboard.html', {
#         'developer_data': developer_data,
#     })
#
# # Job list view
# @login_required
# def job_list(request):
#     jobs = Job.objects.all()
#     return render(request, 'job_list.html', {'jobs': jobs})
#
# # View for deducting balance for a specific developer
# @login_required
# def deduct_balance(request, developer_id):
#     developer = get_object_or_404(User, id=developer_id)
#     tasks = Task.objects.filter(assigned_users=developer)
#
#     if request.method == 'POST':
#         deduction_amount = int(request.POST.get('deduction_amount', 0))
#         current_balance = sum(task.money_for_task for task in tasks if task.paid)
#
#         if deduction_amount <= current_balance:
#             original_deduction_amount = deduction_amount
#
#             for task in tasks.filter(paid=True):
#                 if deduction_amount <= 0:
#                     break
#                 if task.money_for_task <= deduction_amount:
#                     deduction_amount -= task.money_for_task
#                     task.money_for_task = 0
#                 else:
#                     task.money_for_task -= deduction_amount
#                     deduction_amount = 0
#                 task.save()
#
#             DeductionLog.objects.create(
#                 developer=developer,
#                 deducted_by=request.user,
#                 deduction_amount=original_deduction_amount,
#                 deduction_date=now(),
#             )
#
#             messages.success(request, f"Successfully deducted {original_deduction_amount} USD from {developer.username}'s balance.")
#         else:
#             messages.error(request, "Deduction amount exceeds current balance.")
#
#         return redirect('admin_dashboard')
#
#     balance = sum(task.money_for_task for task in tasks if task.paid)
#     return render(request, 'deduct_balance.html', {'developer': developer, 'balance': balance})
#
#
#
# #@login_required
# def developer_tasks(request):
#     developer = request.user  # Assuming each developer is logged in
#     tasks = Task.objects.filter(assigned_users=developer)
#     balance = sum(task.money_for_task for task in tasks if task.paid)
#
#     # Get deduction logs specific to the logged-in developer
#     deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')
#
#     if request.method == 'POST':
#         task_id = request.POST.get('task_id')
#         progress = request.POST.get('progress')
#         feedback = request.POST.get('feedback')
#
#         # Get the task object and update it
#         task = get_object_or_404(Task, id=task_id, assigned_users=developer)
#
#         if progress is not None:
#             task.progress = int(progress)  # Update progress if provided
#         if feedback is not None:
#             task.feedback = feedback  # Update feedback if provided
#
#         task.save()
#
#         # Check if the developer has completed the task (progress = 100%) and handle payment if needed
#         task.check_and_pay_developer()
#
#     return render(request, 'developer_tasks.html', {
#         'developer': developer,
#         'tasks': tasks,
#         'balance': balance,
#         'deduction_logs': deduction_logs
#     })
#
#
#


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
import json
from .models import Job, Task, DeductionLog
from .forms import JobForm, TaskFormSet, ClientLoginForm


# Admin login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the user by email
            user = User.objects.get(email=email)
            # Authenticate using the username (Django default) and password
            if user.check_password(password):
                # Log the user in
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist")
    return render(request, 'login.html')


@login_required
def create_job(request):
    # Check if the logged-in user has the allowed email
    if request.user.email != 'admin_tmk@gmail.com':
        # Return a 403 Forbidden response if the user is not authorized
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            # Hash the client's password before saving
            job.client_password = make_password(job_form.cleaned_data['client_password'])
            job.save()
            return redirect('task_create', job_id=job.id)  # Redirect to task creation
    else:
        job_form = JobForm()

    return render(request, 'create_job.html', {'job_form': job_form})


# @login_required
# def create_tasks(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#
#     if request.method == 'POST':
#         task_formset = TaskFormSet(request.POST, instance=job)
#
#         if task_formset.is_valid():
#             # First, calculate the total hours for all tasks
#             total_hours = sum([form.cleaned_data['hours'] for form in task_formset if form.cleaned_data.get('hours')])
#
#             # Now iterate over the formset and calculate the percentage for each task
#             for form in task_formset:
#                 task = form.save(commit=False)
#                 task.task_percentage = (form.cleaned_data['hours'] / total_hours) * 100
#                 task.save()
#
#             return redirect('job_list')  # Redirect to job list after saving tasks
#     else:
#         task_formset = TaskFormSet(instance=job)
#
#     return render(request, 'create_tasks.html', {
#         'task_formset': task_formset,
#         'job': job,
#     })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from .forms import TaskFormSet

from django.forms import modelformset_factory
from .models import Task




from django.shortcuts import render, get_object_or_404, redirect
from .models import Job
from .forms import TaskFormSet

from django.shortcuts import render, get_object_or_404, redirect
from .models import Job
from .forms import TaskFormSet

def create_tasks(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        task_formset = TaskFormSet(request.POST, instance=job)

        if task_formset.is_valid():
            # Calculate total hours for all tasks
            total_hours = sum([form.cleaned_data['hours'] for form in task_formset if form.cleaned_data.get('hours')])

            # Iterate over the formset and calculate the percentage for each task
            for form in task_formset:
                task = form.save(commit=False)
                task.task_percentage = (form.cleaned_data['hours'] / total_hours) * 100
                task.save()
                form.save_m2m()  # Save ManyToMany relationships, such as assigned users

            return redirect('job_list')  # Redirect to job list after saving tasks
    else:
        task_formset = TaskFormSet(instance=job)

    return render(request, 'create_tasks.html', {
        'task_formset': task_formset,
        'job': job,
    })




@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


def client_login(request):
    if request.method == 'POST':
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Find the job associated with this client
            try:
                job = Job.objects.get(client_email=email)
                if check_password(password, job.client_password):
                    # Store job id in session and redirect to progress page
                    request.session['client_job_id'] = job.id
                    return redirect('client_progress')
                else:
                    messages.error(request, 'Invalid password')
            except Job.DoesNotExist:
                messages.error(request, 'No job found for this email')
    else:
        form = ClientLoginForm()

    return render(request, 'client_login.html', {'form': form})


# @login_required
# def client_progress(request):
#     job_id = request.session.get('client_job_id')
#     if not job_id:
#         return redirect('client_login')
#
#     job = get_object_or_404(Job, id=job_id)
#     tasks = job.tasks.all()
#
#     return render(request, 'client_progress.html', {'job': job, 'tasks': tasks})
#

def client_progress(request):
    job_id = request.session.get('client_job_id')
    if not job_id:
        return redirect('client_login')

    job = get_object_or_404(Job, id=job_id)
    tasks = job.tasks.all()
    months = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь"]

    tasks_data = [
        {
            'title': task.title,
            'start': task.start_date.month - 1 if task.start_date else None,
            'end': task.deadline.month - 1 if task.deadline else None,
            'progress': task.progress
        }
        for task in tasks
    ]

    context = {
        'job': job,
        'tasks': tasks_data,
        'months': months
    }
    return render(request, 'client_progress.html', context)


def developer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate based on email (developers log in using email)
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # Log the developer in
                login(request, user)
                return redirect('developer_tasks')  # Redirect to developer's tasks
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
    return render(request, 'developer_login.html')


@login_required
def developer_tasks(request):
    developer = request.user  # Assuming each developer is logged in
    tasks = Task.objects.filter(assigned_users=developer)
    balance = sum(task.money_for_task for task in tasks if task.paid)
    deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        progress = request.POST.get('progress')

        # Ensure you are fetching the correct task assigned to the developer
        task = get_object_or_404(Task, id=task_id, assigned_users=developer)

        # Update progress only if valid
        if progress is not None:
            task.progress = int(progress)
            task.save()

            # Check if the developer has completed the task (progress = 100%) and handle payment if needed
            if task.progress == 100:
                task.check_and_pay_developer()  # Optional logic for payment

        return redirect('developer_tasks')

    return render(request, 'developer_tasks.html', {
        'developer': developer,
        'tasks': tasks,
        'balance': balance,
        'deduction_logs': deduction_logs
    })

# @login_required
# def developer_tasks(request):
#     developer = request.user  # Assuming each developer is logged in
#     tasks = Task.objects.filter(assigned_users=developer)
#     balance = sum(task.money_for_task for task in tasks if task.paid)
#     deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')
#
#     if request.method == 'POST':
#         # Check if it's an AJAX request to update progress
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             data = json.loads(request.body)
#             task_id = data.get('task_id')
#             progress = data.get('progress')
#
#             # Get the task object and update it
#             task = get_object_or_404(Task, id=task_id, assigned_users=developer)
#
#             if progress is not None:
#                 task.progress = int(progress)  # Update progress if provided
#
#             task.save()
#
#             # Check if the developer has completed the task (progress = 100%) and handle payment if needed
#             if task.progress == 100:
#                 task.check_and_pay_developer()
#
#             return JsonResponse({'success': True})
#         else:
#             # Handle non-AJAX POST requests, e.g., feedback submission
#             task_id = request.POST.get('task_id')
#             feedback = request.POST.get('feedback')
#
#             task = get_object_or_404(Task, id=task_id, assigned_users=developer)
#             if feedback is not None:
#                 task.feedback = feedback  # Update feedback if provided
#                 task.save()
#             # Redirect or render accordingly
#             return redirect('developer_tasks')
#
#     return render(request, 'developer_tasks.html', {
#         'developer': developer,
#         'tasks': tasks,
#         'balance': balance,
#         'deduction_logs': deduction_logs
#     })
#


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import Task, DeductionLog

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import Task, DeductionLog


# @login_required
# def admin_dashboard(request):
#     today = now().date()
#
#     # Get all developers who are staff members
#     developers = User.objects.filter(is_staff=True)
#
#     developer_data = []
#     for developer in developers:
#         # Fetch tasks assigned to this developer
#         tasks = Task.objects.filter(assigned_users=developer)
#
#         # Print statement to check if tasks are being fetched correctly
#         print(f"Developer: {developer.username}, Tasks: {[task.title for task in tasks]}")  # Debugging line
#
#         developer_tasks = [
#             {
#                 'task': task,
#                 'days_until_deadline': (task.deadline - today).days if task.deadline else None
#             }
#             for task in tasks
#         ]
#
#         # Calculate the balance for the developer based on paid tasks
#         balance = sum(task.money_for_task for task in tasks if task.paid)
#
#         developer_data.append({
#             'developer': developer,
#             'tasks': developer_tasks,
#             'balance': balance
#         })
#
#     # Fetch all deduction logs
#     all_deduction_logs = DeductionLog.objects.all().order_by('-deduction_date')
#
#     return render(request, 'admin_dashboard.html', {
#         'developer_data': developer_data,
#         'today': today,
#         'all_deduction_logs': all_deduction_logs
#     })
#


from django.shortcuts import render
from django.utils import timezone
from .models import User, Task, DeductionLog


# def admin_dashboard(request):
#     # Get all developers
#     developers = User.objects.all()
#     developer_data = []
#
#     for developer in developers:
#         # Retrieve tasks assigned to the developer
#         tasks = Task.objects.filter(assigned_users=developer)
#         task_info = []
#
#         for task in tasks:
#             days_until_deadline = None
#             if task.deadline:
#                 days_until_deadline = (task.deadline - timezone.now().date()).days
#
#             task_info.append({
#                 'task': task,
#                 'days_until_deadline': days_until_deadline
#             })
#
#         # Calculate the developer's balance
#         balance = sum(task.money_for_task for task in tasks if task.paid)
#
#         developer_data.append({
#             'developer': developer,
#             'tasks': task_info,
#             'balance': balance
#         })
#
#     # Get all deduction logs
#     all_deduction_logs = DeductionLog.objects.select_related('developer', 'deducted_by').all()
#
#     context = {
#         'developer_data': developer_data,
#         'all_deduction_logs': all_deduction_logs,
#     }
#
#     return render(request, 'admin_dashboard.html', context)
#
#
#
# from django.shortcuts import render
# from django.utils import timezone
# from .models import User, Task, DeductionLog
#
#
# def admin_dashboard(request):
#     developers = User.objects.all()
#     developer_data = []
#
#     # Retrieve all tasks and developers for display
#     tasks = Task.objects.all()
#     for developer in developers:
#         # Get tasks specifically assigned to this developer
#         assigned_tasks = tasks.filter(assigned_users=developer)
#
#         task_info = []
#         for task in assigned_tasks:
#             days_until_deadline = None
#             if task.deadline:
#                 days_until_deadline = (task.deadline - timezone.now().date()).days
#
#             task_info.append({
#                 'task': task,
#                 'days_until_deadline': days_until_deadline
#             })
#
#         # Calculate the developer's balance
#         balance = sum(task.money_for_task for task in assigned_tasks if task.paid)
#
#         developer_data.append({
#             'developer': developer,
#             'tasks': task_info,
#             'balance': balance
#         })
#
#     # Add unassigned tasks for visibility in the dashboard
#     unassigned_tasks = tasks.filter(assigned_users=None)
#     all_deduction_logs = DeductionLog.objects.select_related('developer', 'deducted_by').all()
#
#     context = {
#         'developer_data': developer_data,
#         'unassigned_tasks': unassigned_tasks,
#         'all_deduction_logs': all_deduction_logs,
#     }
#
#     return render(request, 'admin_dashboard.html', context)
#


from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from .models import User, Task, DeductionLog


def admin_dashboard(request):
    developers = User.objects.all()
    developer_data = []

    for developer in developers:
        # Retrieve tasks assigned to the developer
        assigned_tasks = Task.objects.filter(assigned_users=developer)

        # Paginate tasks (show 10 tasks per page)
        paginator = Paginator(assigned_tasks, 5)  # 10 tasks per page
        page_number = request.GET.get(f'page_{developer.id}', 1)  # Unique page param per developer
        page_obj = paginator.get_page(page_number)

        task_info = []
        for task in page_obj:
            days_until_deadline = None
            if task.deadline:
                days_until_deadline = (task.deadline - timezone.now().date()).days

            task_info.append({
                'task': task,
                'days_until_deadline': days_until_deadline
            })

        # Calculate the developer's balance
        balance = sum(task.money_for_task for task in assigned_tasks if task.paid)

        developer_data.append({
            'developer': developer,
            'tasks': task_info,
            'balance': balance,
            'paginator': paginator,  # Add paginator for template access
            'page_obj': page_obj,  # Add page object for current page info
        })

    # Retrieve unassigned tasks
    unassigned_tasks = Task.objects.filter(assigned_users=None)
    all_deduction_logs = DeductionLog.objects.select_related('developer', 'deducted_by').all()

    context = {
        'developer_data': developer_data,
        'unassigned_tasks': unassigned_tasks,
        'all_deduction_logs': all_deduction_logs,
    }

    return render(request, 'admin_dashboard.html', context)


# @login_required
# def admin_dashboard(request):
#     today = now().date()
#
#     # Get all developers who are staff members
#     developers = User.objects.filter(is_staff=True)
#
#     developer_data = []
#     for developer in developers:
#         tasks = Task.objects.filter(assigned_users=developer)
#         developer_tasks = []
#
#         for task in tasks:
#             if task.deadline:
#                 # Calculate days remaining until the deadline
#                 days_until_deadline = (task.deadline - today).days
#             else:
#                 days_until_deadline = None  # Handle tasks without deadlines
#
#             developer_tasks.append({
#                 'task': task,
#                 'days_until_deadline': days_until_deadline
#             })
#
#         # Calculate the current balance for the developer
#         balance = sum(task.money_for_task for task in tasks if task.paid)
#
#         developer_data.append({
#             'developer': developer,
#             'tasks': developer_tasks,
#             'balance': balance
#         })
#
#     # Fetch all deduction logs
#     all_deduction_logs = DeductionLog.objects.all().order_by('-deduction_date')
#
#     return render(request, 'admin_dashboard.html', {
#         'developer_data': developer_data,
#         'today': today,
#         'all_deduction_logs': all_deduction_logs
#     })
#

@login_required
def deduct_balance(request, developer_id):
    developer = get_object_or_404(User, id=developer_id)
    tasks = Task.objects.filter(assigned_users=developer)

    if request.method == 'POST':
        deduction_amount = int(request.POST.get('deduction_amount', 0))
        current_balance = sum(task.money_for_task for task in tasks if task.paid)

        if deduction_amount <= current_balance:
            original_deduction_amount = deduction_amount  # Store the original deduction amount for logging

            for task in tasks.filter(paid=True):
                if deduction_amount <= 0:
                    break
                if task.money_for_task <= deduction_amount:
                    deduction_amount -= task.money_for_task
                    task.money_for_task = 0
                else:
                    task.money_for_task -= deduction_amount
                    deduction_amount = 0
                task.save()

            # Create a log entry
            DeductionLog.objects.create(
                developer=developer,
                deducted_by=request.user,
                deduction_amount=original_deduction_amount,  # Use the original amount for logging
                deduction_date=now(),  # Log the time of deduction
            )

            messages.success(request,
                             f"Successfully deducted {original_deduction_amount} USD from {developer.username}'s balance.")
        else:
            messages.error(request, "Deduction amount exceeds current balance.")
        return redirect('admin_dashboard')

    # Calculate current balance for the developer
    balance = sum(task.money_for_task for task in tasks if task.paid)

    return render(request, 'deduct_balance.html', {
        'developer': developer,
        'balance': balance,
    })


@login_required
def all_deduction_logs(request):
    # Retrieve all deduction logs, ordered by date (latest first)
    logs = DeductionLog.objects.all().order_by('-deduction_date')
    return render(request, 'all_deduction_logs.html', {'deduction_logs': logs})


@login_required
def deduction_logs(request, developer_id):
    developer = get_object_or_404(User, id=developer_id)
    logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')
    return render(request, 'deduction_logs.html', {
        'developer': developer,
        'deduction_logs': logs,
    })
