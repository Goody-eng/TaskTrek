import json
import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  # To protect views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Task, Project  # Import Task and Project models


# Landing Page
def landing_page(request):
    return render(request, 'taskmanager/index.html')

# Signup Page
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Signup successful! Welcome, {user.username}.")
            return redirect('dashboard_page')
        else:
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = UserCreationForm()
    return render(request, 'taskmanager/signup.html', {'form': form})

# Login Page
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard_page')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'taskmanager/login.html', {'form': form})

# Logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('landing_page')

# Contact Page
def contact_page(request):
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # You can save these details to the database or send an email
        messages.success(request, "Your message has been sent successfully!")
        return redirect('landing_page')  # Redirect to landing page after submission
    return render(request, 'taskmanager/contact.html')  # Render the contact form

# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'taskmanager/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_count'] = Task.objects.count()
        context['project_count'] = Project.objects.count()
        return context

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'taskmanager/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter tasks by status
        context['to_do_tasks'] = Task.objects.filter(status='To Do')
        context['doing_tasks'] = Task.objects.filter(status='Doing')
        context['done_tasks'] = Task.objects.filter(status='Done')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'priority', 'status', 'deadline', 'project', 'assignee']
    template_name = 'taskmanager/task_form.html'
    success_url = '/dashboard/'

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'priority', 'status', 'deadline', 'project', 'assignee']
    template_name = 'taskmanager/task_form.html'
    success_url = '/dashboard/'

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskmanager/task_confirm_delete.html'
    success_url = '/dashboard/'

# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'taskmanager/project_list.html'
    context_object_name = 'projects'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'deadline', 'members']
    template_name = 'taskmanager/project_form.html'
    success_url = '/dashboard/'

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'deadline', 'members']
    template_name = 'taskmanager/project_form.html'
    success_url = '/dashboard/'

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'taskmanager/project_confirm_delete.html'
    success_url = '/dashboard/'

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "taskmanager/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all tasks and serialize them for FullCalendar
        tasks = Task.objects.all()
        events = [
            {
                'title': task.name,
                'start': task.deadline.isoformat(),  # Use ISO format for compatibility with FullCalendar
                'url': f"/task/{task.id}/update/"  # Link to the task update page
            }
            for task in tasks
        ]
        context['events'] = json.dumps(events)  # Serialize to JSON for passing to the template
        return context


# API Endpoint for updating task status
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task = Task.objects.get(id=task_id)
            new_status = data.get('status')
            if new_status and new_status in ['To Do', 'Doing', 'Done']:
                task.status = new_status
                task.save()
                return JsonResponse({"message": "Task status updated successfully"}, status=200)
            return JsonResponse({"error": "Invalid status provided"}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)