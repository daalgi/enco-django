from django.urls import path
import projects.views as views

urlpatterns = [
    path('list/', views.projects_list, name='list'),
    path('detail/<int:internal_id>/', views.project_detail, name='detail')
]