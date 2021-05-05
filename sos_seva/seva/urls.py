"""seva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls import include
#from message.admin import event_admin_site

admin.site.site_header = "SEVA Admin"
admin.site.site_title = "SEVA Admin Portal"
admin.site.index_title = "Welcome to SEVA Admin Portal"
#admin.site.site_url = "/seva_api/"
urlpatterns = [
    #url(r'^', admin.site.urls),
    path('WhatsAppUsers/', include('message.urls',namespace='message_api')),
    url(r'seva_admin/', admin.site.urls),
    path('', include('signup.urls')),
    # path('isb_db/', include('isb_db.urls', namespace='isb_db')),
    path('search/', include('isb_db.urls', namespace='search')),
    path('informer/', include('informer.urls', namespace='informer')),
    #path('seva_api/seva_admin/', admin.site.urls)
]

#print(urlpatterns)

#print("admin",admin.site.urls)
