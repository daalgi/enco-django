from django.urls import path
from projects.views import DashBoard

urlpatterns = [
    path('dashboard/', DashBoard.as_view(), name='dashboard')
]