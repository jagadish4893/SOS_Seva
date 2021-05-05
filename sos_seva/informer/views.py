from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import tweet
from .tweet_scraper import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def ticket_dashboard(request):
    return redirect('/seva_admin/message/whatsappusers')


@csrf_exempt
def get_ques(request):
    # TODO: Fix key error, question from template being returned correctly
#    ques = request.POST.get('ques', None)
    if request.method == "POST":
        print("inside post")
        ques = request.POST.get('ques', None)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=2)
        data = tweet.objects.filter(date__range=[start_date, end_date]).values()
        similarity_vals = similarity(ques, data)
        similarity_dict = {"tweet": similarity_vals}
        print(similarity_dict)
        return JsonResponse({'tweets': similarity_vals}, safe=False)
    else:
        print("outside post")
        return JsonResponse({'tweets': "Error"}, safe=False)



#1) Chron job script
#2) Data reading in views.py
#3) Passing the data through similarity funciton
#4) Change in index.html based on the dicitonary created in views.py