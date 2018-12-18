from django.urls import path
from projects.views import ProjectsList

urlpatterns = [
    path('', ProjectsList.as_view(), name='list')
]