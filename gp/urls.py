from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('create_alphanumeric/', views.create_alphanumeric, name='create_alphanumeric'),
    path('create_passpoints/', views.create_passpoints, name='create_passpoints'),
    path('create_passpoints2/', views.create_passpoints2, name='create_passpoints2'),
    path('create_new_passpoints/', views.create_new_passpoints, name='create_new_passpoints'),
    path('create_new_passpoints2/', views.create_new_passpoints2, name='create_new_passpoints2'),
    path('confirm_alphanumeric/', views.confirm_alphanumeric, name='confirm_alphanumeric'),
    path('confirm_passpoints/', views.confirm_passpoints, name='confirm_passpoints'),
    path('confirm_new_passpoints/', views.confirm_new_passpoints, name='confirm_new_passpoints'),
    path('test_alphanumeric/', views.test_alphanumeric, name='test_alphanumeric'),
    path('test_passpoints/', views.test_passpoints, name='test_passpoints'),
    path('test_passpoints2/', views.test_passpoints2, name='test_passpoints2'),
    path('test_new_passpoints/', views.test_new_passpoints, name='test_new_passpoints'),
    path('test_new_passpoints2/', views.test_new_passpoints2, name='test_new_passpoints2'),
    path('survey/', views.sus, name='sus'),
    path('success/', views.success, name='success')

]