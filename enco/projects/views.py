from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from projects.models import Project

#from projects.models import Project

# class ProjectsList(TemplateView):
#     template_name = 'projects\list.html'

#     def get(self, request):
#         projects = Project.objects.all()
#         args = {'projects': projects}
#         return render(request, self.template_name, args)

def projects_list(request):
    projects = Project.objects.all()
    args = {'projects': projects}
    return render(request, 'projects/list.html', args)

def project_detail(request, internal_id):
    project = Project.objects.get(internal_id=internal_id)
    args = {'project': project}
    return render(request, 'projects/detail.html', args)