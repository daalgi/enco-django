from django.shortcuts import render, redirect
#from django.views.generic import TemplateView


def home(request):
    args = {}
    return render(request, 'home/home.html', args)