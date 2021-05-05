from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.user_login, name='role_login'),
    path('authenticateUser', views.authenticateUser, name='authenticateUser'),
    path('logout', views.user_logout, name='user_logout'),
    path('register',views.register,name='register'),
    ]

app_name = 'signup'