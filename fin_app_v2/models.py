# # # # from django.db import models
# # # # from django.contrib.auth.models import User
# # # #
# # # # class Job(models.Model):
# # # #     title = models.CharField(max_length=100)
# # # #     client_email = models.EmailField(unique=True)  # Ensure client email is unique
# # # #     client_password = models.CharField(max_length=100)  # Store a hashed password for security
# # # #     assigned_users = models.ManyToManyField(User, related_name='developer_jobs')
# # # #
# # # #     def __str__(self):
# # # #         return self.title
# # # #
# # # #
# # # # class Task(models.Model):
# # # #     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tasks')
# # # #     title = models.CharField(max_length=100)
# # # #     assigned_users = models.ManyToManyField(User, related_name='developer_tasks')
# # # #     description = models.TextField()
# # # #
# # # #     def __str__(self):
# # # #         return self.title
# # # from django.db import models
# # # from django.contrib.auth.models import User
# # #
# # # class Job(models.Model):
# # #     title = models.CharField(max_length=100)
# # #     client_email = models.EmailField(unique=True)
# # #     client_password = models.CharField(max_length=100)
# # #
# # #     def __str__(self):
# # #         return self.title
# # #
# # #     def get_overall_progress(self):
# # #         total_percentage = 0
# # #         total_weight = 0
# # #         tasks = self.tasks.all()
# # #
# # #         for task in tasks:
# # #             total_percentage += task.progress * (task.task_percentage / 100)
# # #             total_weight += task.task_percentage
# # #
# # #         # Calculate weighted progress
# # #         return (total_percentage / total_weight) if total_weight > 0 else 0
# # #
# # #
# # # class Task(models.Model):
# # #     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tasks')
# # #     title = models.CharField(max_length=100)
# # #     description = models.TextField()
# # #     assigned_users = models.ManyToManyField(User, related_name='developer_tasks')
# # #
# # #     task_percentage = models.PositiveIntegerField()  # Percentage of the project this task represents
# # #     progress = models.PositiveIntegerField(default=0)  # Developer's progress on this task
# # #
# # #     def __str__(self):
# # #         return self.title
# #
# #
# # from django.db import models
# # from django.contrib.auth.models import User
# #
# # class Job(models.Model):
# #     title = models.CharField(max_length=100)
# #     client_email = models.EmailField(unique=True)
# #     client_password = models.CharField(max_length=100)
# #
# #     def __str__(self):
# #         return self.title
# #
# #     def get_overall_progress(self):
# #         total_percentage = 0
# #         total_weight = 0
# #         tasks = self.tasks.all()
# #
# #         for task in tasks:
# #             total_percentage += task.progress * (task.task_percentage / 100)
# #             total_weight += task.task_percentage
# #
# #         return (total_percentage / total_weight) if total_weight > 0 else 0  # Return the weighted overall progress
# #
# #
# # class Task(models.Model):
# #     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tasks')
# #     title = models.CharField(max_length=100)
# #     description = models.TextField()
# #     assigned_users = models.ManyToManyField(User, related_name='developer_tasks')
# #
# #     task_percentage = models.PositiveIntegerField()  # Percentage this task represents in the project
# #     progress = models.PositiveIntegerField(default=0)  # Developer's current progress (0-100%)
# #
# #     def __str__(self):
# #         return self.title
# from django.db import models
# from django.contrib.auth.models import User
#
# class Job(models.Model):
#     title = models.CharField(max_length=100)
#     client_email = models.EmailField(unique=True)
#     client_password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.title
#
#     def get_overall_progress(self):
#         total_percentage = 0
#         total_weight = 0
#         tasks = self.tasks.all()
#
#         for task in tasks:
#             total_percentage += task.progress * (task.task_percentage / 100)
#             total_weight += task.task_percentage
#
#         return (total_percentage / total_weight) if total_weight > 0 else 0  # Return the weighted overall progress
#
#
# class Task(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tasks')
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     assigned_users = models.ManyToManyField(User, related_name='developer_tasks')
#
#     task_percentage = models.PositiveIntegerField()  # Percentage this task represents in the project
#     progress = models.PositiveIntegerField(default=0)  # Developer's current progress (0-100%)
#     deadline = models.DateField(null=True, blank=True)  # Deadline for the task
#
#     def __str__(self):
#         return self.title
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=100)
    client_email = models.EmailField(unique=True)
    client_password = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_overall_progress(self):
        total_percentage = 0
        total_weight = 0
        tasks = self.tasks.all()

        for task in tasks:
            total_percentage += task.progress * (task.task_percentage / 100)
            total_weight += task.task_percentage

        return (total_percentage / total_weight) if total_weight > 0 else 0  # Return the weighted overall progress


class Task(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_users = models.ManyToManyField(User, related_name='developer_tasks')

    task_percentage = models.PositiveIntegerField()  # Percentage this task represents in the project
    progress = models.PositiveIntegerField(default=0)  # Developer's current progress (0-100%)
    deadline = models.DateField(null=True, blank=True)  # Deadline for the task
    feedback = models.TextField(blank=True, null=True)  # Feedback from developer

    def __str__(self):
        return self.title
