from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('twitter', views.index, name='twitter_search'),
    path('get_ques', views.get_ques, name='get_ques'),
    path('ticket_dashboard', views.ticket_dashboard, name='ticket_dashboard'),
    # url(r'^info_ret', views.information_ret.as_view(), name='info_ret'),
]

app_name = 'informer'