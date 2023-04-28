from django.urls import path
from checklists import views

urlpatterns = [
    path('', views.TodolistView.as_view(), name="todolist_view"),
    path('mytodolist/', views.TodolistDetailView.as_view(), name="mytodolist_view"),
    path('mytodolist/<int:todolist_id>/', views.TodolistDetailView.as_view(), name="mytodolist_updateordelete_view"),
]