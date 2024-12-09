from django.db import models
from django.contrib.auth.models import User  # Using the built-in User model for user authentication

# Model for Project
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

# Model for Task
class Task(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Low', 'Low'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='To Do')
    deadline = models.DateField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Model for Comment
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Link to Task
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User (commenter)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.task}'

# Model for Notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User (receiver of notification)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Flag to track whether the notification is read

    def __str__(self):
        return f'Notification for {self.user}'
