from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth



# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        request.session['is_logged'] = False
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            messages.info(request, 'Invalid Credentials')
            return render(request, "login.html")
        else:
            login(request, user)
            request.session['is_logged'] = True
            request.session['username'] = username
            request.session['first_name'] = request.user.first_name
            request.session['last_name'] = request.user.last_name
            return redirect('isb_db:dashboard')

    else:
        # import pdb;pdb.set_trace()
        if request.user.is_authenticated:
            request.session['is_logged'] = True
            request.session['username'] = request.user.username
            request.session['first_name'] = request.user.first_name
            request.session['last_name'] = request.user.last_name
            return redirect('isb_db:dashboard')
        else:
            return render(request, 'login.html')



@csrf_exempt
def authenticateUser(request):
     return redirect("insect:insect_dashboard")

def user_logout(request):
    logout(request)
    return redirect('signup:role_login')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already registered')
                return redirect('signup:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('signup:register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name)
                user.save();
                messages.info(request,'User created successfully')
                return redirect('signup:role_login')
        else:
            messages.info(request,'Password mismatch')
            return redirect('signup:register')
    else:
        return render(request,'register.html')



