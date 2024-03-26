from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path('delete/<int:task_index>/', views.delete_task, name='delete_task'),
]
