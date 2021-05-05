from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    url(r'^info_ret', views.information_ret.as_view(), name='info_ret'),
    url(r'^get_details/$', views.get_details, name='get_details'),
    url(r'^update_info/$', views.update_database, name='update_info'),
    url(r'^new_resource/$', views.new_resource, name='new_resource')
]

app_name = 'isb_db'