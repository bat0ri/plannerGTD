
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('add_label/', views.add_label, name='add_label'),
    path('delete_label/<int:label_id>/', views.delete_label, name='delete_label'),

]
