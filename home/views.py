from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from redbus.models import buses
from django.contrib.auth import login, logout, authenticate
def home(request):
    return render(request, 'home.html')
'''
def profile(request):
    messages.SUCCESS(request,"WELCOME TO PROFILE")
    if request.method =='post':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        print('h')
        profile = profile(name = name, email = email, phone = phone)
        profile.save()
    return render(request, 'profile.html')'''

def search(request):
    query = request.GET['query']
    will = request.GET['will']
    if len(query) == 0 or len(will) == 0:
        messages.warning(request, 'Please enter something to search')
        return redirect("/")
    else:
        pos = buses.objects.filter(city1__icontains=query, city2__icontains=will)
    posts = {'pos': pos}
    return render(request, "search.html", posts)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if not username.isalnum():
            messages.warning("The username can only contain alphanmeric values.")
            return redirect("/")
        if pass1 != pass2:
            messages.warning(request,"The passwords do not match")
            return redirect('/')
        myuser = User.objects.create_user(username, email ,pass1)
        myuser.save()
        messages.success(request, "Your account has been created!")
        return redirect("/") 
    else:
        return HttpResponse("I")   

def hlogin(request):
    if request.method == 'POST':
        username1 = request.POST['username1']
        pass1 = request.POST['pass11']
        user = authenticate(username = username1, password = pass1)
        
        if user is not None:
            login(request,user)
            messages.success(request, "You are succesfully logged in!")
            return redirect('/')
        else:
            messages.warning(request, "Credentials do not match, PLease Try Again")
            return redirect('/') 
def hlogout(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('/')