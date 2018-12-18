from django.shortcuts import render, redirect
from django.views.generic import TemplateView

#from projects.models import Project

class ProjectsList(TemplateView):
    template_name = 'projects\list.html'

    def get(self, request):
        #projects = Project.objects.all()
        
        args = {}#{'projects': projects}
        return render(request, self.template_name, args)
       
