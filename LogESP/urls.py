"""LogESP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from LogESP import views

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('license/', login_required(
        TemplateView.as_view(template_name='license.html')),
        name='license'),
    path('hwam/', include('hwam.urls')),
    path('risk/', include('risk.urls')),
    path('siem/', include('siem.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('accounts/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    #path('accounts/password_change/done/', auth_views., name=''),
    path('admin/', admin.site.urls),
]
