from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('family/create/', views.create_family, name='create_family'),
    path('family/join/', views.join_family, name='join_family'),
    path('family/share/', views.share_family, name='share_family'),
    path('family/leave/', views.leave_family, name='leave_family'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('records/', views.records, name='records'),
    path('records/add/', views.create, name='create'),
    path('records/<str:pk>/edit/', views.edit, name='edit'),
    path('records/<str:pk>/delete/', views.delete, name='delete'),
]
