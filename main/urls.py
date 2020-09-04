from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('records/', views.records, name='records'),
    path('records/add/', views.create, name='create'),
    path('records/<str:pk>/edit/', views.edit, name='edit'),
    path('records/<str:pk>/delete/', views.delete, name='delete'),
]
