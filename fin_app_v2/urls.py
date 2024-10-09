from django.urls import path
from .views import create_job, create_tasks, job_list, client_login, client_progress,developer_login,developer_tasks

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
]
