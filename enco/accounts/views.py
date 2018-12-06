from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def signup(request):
        if request == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        form.save()
                        username = form.cleaned_data.get('username')
                        raw_password = form.cleaned_data('password1')
                        user = authenticate(username=username, password=raw_password)
                        login(request, user)
                        return redirect(reverse('projects:dashboard'))
        else:
                form = UserCreationForm()
                args = {'form': form}
                return render(request, 'accounts/signup.html', args)