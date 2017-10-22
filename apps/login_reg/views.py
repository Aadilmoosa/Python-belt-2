from django.shortcuts import render, redirect, HttpResponse

from .models import *

from django.contrib import messages

# ===================================================
#                   Render
# ===================================================

def index(request):
    return render(request, "login_reg/index.html")

def home(request):
    if 'userID' not in request.session:
        return redirect("/")

    user = User.objects.get(id=request.session['userID'])
    return render(request, "login_reg/home.html", {'user': user})

    


# ===================================================
#                   Process
# ===================================================

def register(request):
    errors = User.objects.regvalidation(request.POST)

    if errors:
        for key, message in errors.iteritems():
            messages.error(request, message, extra_tags=key)
        return redirect("/")
   
    user = User.objects.newUser(request.POST)
    request.session['userID'] = user.id
    return redirect("/home")

def login(request):
    user = User.objects.login(request.POST)
    if user:
        request.session['userID'] = user.id
        return redirect('/home')

    messages.error(request,"email or password invalid", extra_tags="login") 
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')