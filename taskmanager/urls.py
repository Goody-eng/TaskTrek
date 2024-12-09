from django.urls import path
from . import views
from .views import CalendarView

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing page
    path('signup/', views.signup_page, name='signup_page'),  # Signup page
    path('login/', views.login_page, name='login_page'),  # Login page
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_page'),  # Protected Dashboard
    path('contact/', views.contact_page, name='contact_page'),  # Contact page
    path('logout/', views.logout_user, name='logout_user'),  # Logout functionality
    path('tasks/', views.TaskListView.as_view(), name='task_list'),  # Task list
    path('task/new/', views.TaskCreateView.as_view(), name='task_create'),  # Create task
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),  # Update task
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),  # Delete task
    path('tasks/update-status/<int:task_id>/', views.update_task_status, name='update_task_status'),  # Update task status
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
]
