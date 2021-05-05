from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^message$', views.broadcast_sms, name="default"),
    path('listen/', views.incoming_message, name='webhook_message'),
]

app_name = 'message'