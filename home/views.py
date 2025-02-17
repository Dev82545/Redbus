from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from redbus.models import buses, Seat_booked, stop
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import WalletTopUpForm
from .models import Wallet
def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    t = Seat_booked.objects.filter(user = request.user)
    h = request.user
    se = {'t': t}
    return render(request, 'profile.html', se)

def search(request):
    query = request.GET['query']
    will = request.GET['will']
    if len(query) == 0 or len(will) == 0:
        messages.warning(request, 'Please enter something to search')
        return redirect("/")
    else:
        pos = buses.objects.filter(stop__stop__icontains=query)\
                     .filter(stop__stop__icontains=will)\
                     .distinct()
        
        if not pos.exists():
            messages.warning(request, 'No bus run between the 2 cities')
            return redirect("/")
        
        posts = {'pos': pos}
        return render(request, "search.html", posts)
  
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if not username.isalnum():
            messages.warning(request, "The username can only contain alphanmeric values.")
            return redirect("/")
        if pass1 != pass2:
            messages.warning(request,"The passwords do not match")
            return redirect('/')
        if User.objects.filter(username=username).exists():
            messages.warning(request, "This username is already taken. Please try another one.")
            return redirect("/")
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        login(request, myuser)
        messages.success(request, f"Your account has been created!,{username}")
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
    else:
        messages.warning (request, " Please Login to book seats")
        return redirect('/')
         
def hlogout(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('/')

@login_required
def wallet_topup(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        form = WalletTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet.balance += amount
            wallet.save()
            messages.success(request, f"${amount} has been added to your wallet!")
            return redirect('profile')  # or another page
    else:
        form = WalletTopUpForm()
        context = {'form': form, 'wallet': wallet}
    return render(request, 'wallet_topup.html', context)

def cancel(request, booking_id):
    cancel = get_object_or_404(Seat_booked, id=booking_id, user=request.user)
    if request.method == 'POST':
        bus = cancel.buses
        bus.seats += cancel.seat_number
        bus.luxury_seats += cancel.lseat_number
        bus.sleeper_seats += cancel.sseat_number
        bus.save()
        refund_amount = (
            cancel.seat_number * bus.seats_cost +
            cancel.lseat_number * bus.sleeper_seats_cost +
            cancel.sseat_number * bus.luxury_seats_cost
        )
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += refund_amount
        wallet.save()
        
        cancel.delete()
        
        messages.success(request, "Your booking has been cancelled and a refund has been processed.")
        return redirect("profile")
    else:
        return redirect('/')