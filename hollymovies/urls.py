"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from viewer.views import hello, simple_hello, movies_list, MoviesView, MovieCreateView, MyPasswordChangeView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helloUrl/<name>', hello),
    path('helloUrl', hello),
    path('', MoviesView.as_view(),  name='index'),
    path('movie/create', MovieCreateView.as_view(), name='create_movie'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/change_pass/', MyPasswordChangeView.as_view(), name='change_pass'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign_up/', SignUpView.as_view(), name='sign_up')

]
