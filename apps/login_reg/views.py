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

# ===================================================

def quotes(request):
    user = User.objects.get(id=request.session['userID'])

    context = {
        'user': user,
        'quotable_quotes': Quote.objects.exclude(favorites = user),
        'favorites': user.favorites.all()
    }
    print Quote.objects.all()
    return render(request, 'login_reg/quotes.html', context)
    
    # return render(request, "login_reg/quotes.html", {'user': user})


def create(request):
    check = Quote.objects.validateQuote(request.POST)

    if check:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="add_item")

    else:
        user = User.objects.get(id=request.session['userID'])
        quote = Quote.objects.create(
            content = request.POST['content'],
            poster = user,
            # author = request.POST['author']
            )
        print "quote", quote

    return redirect('/quotes')


def add_favorite(request,id):
    user = User.objects.get(id=request.session['userID'])
    favorite = Quote.objects.get(id=id)

    user.favorites.add(favorite)

    return redirect('/quotes')


def delete_favorite(request,id):
    user = User.objects.get(id=request.session['userID'])
    favorite = Quote.objects.get(id=id)

    user.favorites.remove(favorite)

    return redirect('/quotes')

def show_user(request,id):
    user =  User.objects.get(id = id)
    context = { 'user': user }
    print context
    return render(request, 'login_reg/user.html', context)

def show_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    context = {
        'quote': quote,
        'users':quote.favorites.all().exclude(id = request.session['userID'])
    }
    return render(request, 'login_reg/item.html', context)