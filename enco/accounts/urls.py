from django.urls import path
from django.contrib.auth import views as auth_views
import accounts.views

urlpatterns = [
    path('signup/', accounts.views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]