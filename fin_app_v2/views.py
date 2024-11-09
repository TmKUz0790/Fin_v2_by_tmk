
from datetime import timezone
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
from .forms import TaskFormSet
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User
from collections import Counter
from django.utils import timezone
from .models import Task, DeductionLog
from django.forms import modelformset_factory
from .models import Task

from django.shortcuts import render, get_object_or_404, redirect
from .models import Job
from .forms import TaskFormSet

from django.shortcuts import render, get_object_or_404, redirect
from .models import Job
from .forms import TaskFormSet
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


def job_list(request):
    # Retrieve all jobs
    jobs = Job.objects.all()

    # Set up pagination for jobs (10 jobs per page)
    paginator = Paginator(jobs, 20)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)

    return render(request, 'job_list.html', {
        'jobs': page_jobs,  # Pass the paginated jobs
    })


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


# @login_required
# def developer_tasks(request):
#     developer = request.user  # Assuming each developer is logged in
#     tasks = Task.objects.filter(assigned_users=developer)
#     balance = sum(task.money_for_task for task in tasks if task.paid)
#     deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')
#
#     if request.method == 'POST':
#         task_id = request.POST.get('task_id')
#         progress = request.POST.get('progress')
#
#         # Ensure you are fetching the correct task assigned to the developer
#         task = get_object_or_404(Task, id=task_id, assigned_users=developer)
#
#         # Update progress only if valid
#         if progress is not None:
#             task.progress = int(progress)
#             task.save()
#
#             # Check if the developer has completed the task (progress = 100%) and handle payment if needed
#             if task.progress == 100:
#                 task.check_and_pay_developer()  # Optional logic for payment
#
#         return redirect('developer_tasks')
#
#     return render(request, 'developer_tasks.html', {
#         'developer': developer,
#         'tasks': tasks,
#         'balance': balance,
#         'deduction_logs': deduction_logs
#     })

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, DeductionLog

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task, DeductionLog

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task, DeductionLog

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task, DeductionLog

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task, DeductionLog

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task, DeductionLog

@login_required
def developer_tasks(request):
    developer = request.user

    # Sort tasks by deadline in ascending order and paginate for main task list
    tasks = Task.objects.filter(assigned_users=developer).order_by('deadline')
    paginator = Paginator(tasks, 7)  # Main task list pagination
    page_number = request.GET.get('page')
    page_tasks = paginator.get_page(page_number)

    # Pagination for Feedback Tasks
    feedback_paginator = Paginator(tasks, 10)  # Paginate feedback section, 3 tasks per page
    feedback_page_number = request.GET.get('feedback_page')
    feedback_page_tasks = feedback_paginator.get_page(feedback_page_number)

    balance = sum(task.money_for_task for task in tasks if task.paid)
    deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        progress = request.POST.get('progress')
        task = get_object_or_404(Task, id=task_id, assigned_users=developer)

        if progress is not None:
            task.progress = int(progress)
            task.save()

            if task.progress == 100:
                task.check_and_pay_developer()

        return redirect('developer_tasks')

    return render(request, 'developer_tasks.html', {
        'developer': developer,
        'tasks': page_tasks,
        'feedback_tasks': feedback_page_tasks,  # Pass paginated feedback tasks to the template
        'balance': balance,
        'deduction_logs': deduction_logs
    })

@login_required
def payment_history(request):
    developer = request.user
    deduction_logs = DeductionLog.objects.filter(developer=developer).order_by('-deduction_date')

    return render(request, 'payment_history.html', {
        'developer': developer,
        'deduction_logs': deduction_logs
    })

# def admin_dashboard(request):
#     # Get all developers
#     developers = User.objects.all()
#     developer_data = []
#
#     # Loop through each developer to gather task data
#     for developer in developers:
#         assigned_tasks = Task.objects.filter(assigned_users=developer)
#
#         # Count task statuses for all tasks assigned to the developer
#         status_counter = Counter({'task_green': 0, 'task_yellow': 0, 'task_red': 0, 'overdue': 0})
#
#         for task in assigned_tasks:
#             days_until_deadline = None
#             if task.deadline:
#                 days_until_deadline = (task.deadline - timezone.now().date()).days
#
#             # Determine task color based on deadline or completion
#             task_color = None
#             if task.progress == 100:
#                 task_color = 'done'
#             elif days_until_deadline is not None:
#                 if days_until_deadline > 10:
#                     task_color = 'task_green'
#                 elif 5 < days_until_deadline <= 10:
#                     task_color = 'task_yellow'
#                 elif 0 <= days_until_deadline <= 5:
#                     task_color = 'task_red'
#                 else:
#                     task_color = 'overdue'
#
#             if task_color and task_color != 'done':  # Only count tasks that aren't marked as 'done'
#                 status_counter[task_color] += 1
#
#         # Paginate tasks for each developer (5 tasks per page for each developer)
#         task_paginator = Paginator(assigned_tasks, 5)
#         page_number = request.GET.get(f'page_{developer.id}', 1)
#         page_obj = task_paginator.get_page(page_number)
#
#         # Create task info including days until deadline
#         task_info = [{
#             'task': task,
#             'days_until_deadline': (task.deadline - timezone.now().date()).days if task.deadline else None
#         } for task in page_obj]
#
#         # Calculate the balance based on paid tasks
#         balance = sum(task.money_for_task for task in assigned_tasks if task.paid)
#
#         developer_data.append({
#             'developer': developer,
#             'tasks': task_info,
#             'balance': balance,
#             'paginator': task_paginator,
#             'page_obj': page_obj,
#             'status_counts': status_counter,  # Pass the full task status count
#         })
#
#     # Paginate the list of developers (5 developers per page)
#     developers_paginator = Paginator(developer_data, 2)
#     developers_page_number = request.GET.get('developer_page', 1)
#     developers_page_obj = developers_paginator.get_page(developers_page_number)
#
#     # Unassigned tasks and all deduction logs
#     unassigned_tasks = Task.objects.filter(assigned_users=None)
#     all_deduction_logs = DeductionLog.objects.select_related('developer', 'deducted_by').all()
#
#     context = {
#         'developer_data': developers_page_obj,  # Pass paginated developer data
#         'unassigned_tasks': unassigned_tasks,
#         'all_deduction_logs': all_deduction_logs,
#     }
#
#     return render(request, 'admin_dashboard.html', context)
#

from collections import Counter
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from .models import User, Task, DeductionLog

def admin_dashboard(request):
    # Get all developers
    developers = User.objects.all()
    developer_data = []

    # Loop through each developer to gather task data
    for developer in developers:
        assigned_tasks = Task.objects.filter(assigned_users=developer)
        status_counter = Counter({'task_green': 0, 'task_yellow': 0, 'task_red': 0, 'overdue': 0})

        # Prepare task info with color coding and deadline calculation
        task_info = []
        for task in assigned_tasks:
            days_until_deadline = (task.deadline - timezone.now().date()).days if task.deadline else None
            task_color = 'done' if task.progress == 100 else None

            # Set task color based on deadline and progress
            if task_color is None and days_until_deadline is not None:
                if days_until_deadline > 10:
                    task_color = 'task_green'
                elif 5 < days_until_deadline <= 10:
                    task_color = 'task_yellow'
                elif 0 <= days_until_deadline <= 5:
                    task_color = 'task_red'
                else:
                    task_color = 'overdue'

            # Add non-done tasks to the status counter
            if task_color and task_color != 'done':
                status_counter[task_color] += 1

            task_info.append({
                'task': task,
                'days_until_deadline': days_until_deadline,
                'color': task_color  # Pass color for easier frontend rendering
            })

        # Paginate tasks per developer (5 tasks per page)
        task_paginator = Paginator(task_info, 5)
        page_number = request.GET.get(f'page_{developer.id}', 1)
        page_obj = task_paginator.get_page(page_number)

        # Calculate balance based on paid tasks
        balance = sum(task.money_for_task for task in assigned_tasks if task.paid)

        developer_data.append({
            'developer': developer,
            'tasks': page_obj,
            'balance': balance,
            'status_counts': status_counter,
        })

    # Paginate developers (5 developers per page)
    developers_paginator = Paginator(developer_data, 2)
    developers_page_number = request.GET.get('developer_page', 1)
    developers_page_obj = developers_paginator.get_page(developers_page_number)

    # Fetch unassigned tasks and deduction logs
    unassigned_tasks = Task.objects.filter(assigned_users=None)
    all_deduction_logs = DeductionLog.objects.select_related('developer', 'deducted_by').all()

    context = {
        'developer_data': developers_page_obj,
        'unassigned_tasks': unassigned_tasks,
        'all_deduction_logs': all_deduction_logs,
    }

    return render(request, 'admin_dashboard.html', context)


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Job, Task
from django.db.models import Max, Sum

def job_details(request, job_id):
    # Fetch the specific job or return a 404 error if not found
    job = get_object_or_404(Job, id=job_id)

    # Retrieve all tasks associated with this job
    tasks = Task.objects.filter(job=job)

    # Set up pagination for tasks (10 tasks per page)
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_tasks = paginator.get_page(page_number)

    # Calculate the latest deadline across all tasks if tasks are available
    latest_deadline = tasks.aggregate(Max('deadline'))['deadline__max'] if tasks else None

    # Get the overall progress of the job
    overall_progress = job.get_overall_progress()

    # Calculate the total payment for all tasks
    total_task_payment = tasks.aggregate(Sum('money_for_task'))['money_for_task__sum'] or 0

    # Calculate the remaining income
    remaining_income = job.over_all_income - total_task_payment

    return render(request, 'job_details.html', {
        'job': job,
        'tasks': page_tasks,  # Pass the paginated tasks
        'latest_deadline': latest_deadline,
        'overall_progress': overall_progress,
        'total_task_payment': total_task_payment,
        'remaining_income': remaining_income,
    })

from django.shortcuts import render
from .models import DeductionLog


def deduction_logs_admin(request):
    # Fetch all users for the user filter dropdown
    users = User.objects.all()

    # Get unique months from DeductionLog dates
    all_deduction_logs = DeductionLog.objects.all()
    months = all_deduction_logs.dates('deduction_date', 'month')

    # Get selected user and month from the request parameters
    selected_user = request.GET.get('user')
    selected_month = request.GET.get('month')

    # Apply filters
    if selected_user:
        all_deduction_logs = all_deduction_logs.filter(developer__id=selected_user)
    if selected_month:
        year, month = map(int, selected_month.split('-'))
        all_deduction_logs = all_deduction_logs.filter(deduction_date__year=year, deduction_date__month=month)

    return render(request, 'deduction_logs_admin.html', {
        'all_deduction_logs': all_deduction_logs,
        'users': users,
        'months': months,
        'selected_user': selected_user,
        'selected_month': selected_month,
    })

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

def deduction_page(request):
    # Retrieve all developers
    developers = User.objects.all()

    return render(request, 'deduction_page.html', {
        'developers': developers,
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
