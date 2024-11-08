from django.urls import path

from . import views
from .views import (create_job, create_tasks, job_list, client_login, client_progress,developer_login,developer_tasks,admin_dashboard,
                    deduction_logs,all_deduction_logs,deduct_balance,login_view)

urlpatterns = [
    # Job creation (no developers assigned here)
    path('jobs/create/', create_job, name='create_job'),

    # Task creation (developers assigned here)
    path('jobs/<int:job_id>/tasks/create/', create_tasks, name='task_create'),

    # View job list
    path('jobs/', job_list, name='job_list'),

    # Client login
    path('client/login/', client_login, name='client_login'),

    # Client progress (view tasks for a job)
    path('client/progress/', client_progress, name='client_progress'),

    path('developer/login/', developer_login, name='developer_login'),
    path('developer/tasks/', developer_tasks, name='developer_tasks'),
    path('deduction_logs/<int:developer_id>/', deduction_logs, name='deduction_logs'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('deduct-balance/<int:developer_id>/', deduct_balance, name='deduct_balance'),
    path('job-list/', job_list, name='job_list'),
    path('', login_view, name='login'),

# Admin login URL
    path('login/', views.login_view, name='login'),

    # Job creation URLs
    path('create_job/', views.create_job, name='create_job'),
    path('task_create/<int:job_id>/', views.create_tasks, name='task_create'),

    # Job list URL
    path('job_list/', views.job_list, name='job_list'),

    # Client URLs
    path('client_login/', views.client_login, name='client_login'),
    path('client_progress/', views.client_progress, name='client_progress'),

    # Developer URLs
    path('developer_login/', views.developer_login, name='developer_login'),
    path('developer_tasks/', views.developer_tasks, name='developer_tasks'),
    path('update_progress/', views.developer_tasks, name='update_progress'),  # For AJAX progress updates

    # Admin dashboard URL
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Deduct balance URL
    path('deduct_balance/<int:developer_id>/', views.deduct_balance, name='deduct_balance'),

    path('deduction-logs/', all_deduction_logs, name='all_deduction_logs'),
    #path('deduction_logs/<int:developer_id>/', deduction_logs, name='deduction_logs'),

]
