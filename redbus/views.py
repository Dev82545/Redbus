from django.shortcuts import render, HttpResponse, redirect
from .models import buses
from django.contrib import messages

def redbus(request):
    allposts = buses.objects.all()
    context = {'allposts': allposts}
    return render(request, 'redbus.html',context)

def red(request,slug):
    bus = buses.objects.filter(slug = slug).first()
    context = {'bus':bus}
    return render(request, 'red.html', context)

def seat(request,slug):
    f =buses.objects.filter(slug = slug).first()
    query = request.GET['query']
    que = request.GET['que']
    tue = request.GET['tue']
    query =int(query)
    que =int(que)
    tue =int(tue)
    seat = int(f.seats)
    lseat = int(f.luxury_seats)
    sseat = int(f.sleeper_seats)
    if query > seat or que > lseat or tue > sseat:
        messages.warning(request, 'Choose the amount of seats available')
        return redirect('/')
    else:
        f.luxury_seats -= que
        f.sleeper_seats -= tue
        f.seats -= query
        f.save()
        messages.success(request, 'Seats selected successfully!')
        return redirect('/')

'''
def seat(request,slug):
    f =buses.objects.filter(slug = slug).first()
    query = request.GET['query']
    
        messages.warning(request, 'Choose the amount of seats available')
        return redirect('red')
    else:
        f.seats -= query
        f.save()
        messages.success(request, 'Seats selected successfully!')
        return redirect('/')
    if seat == 0:  # ✅ Handle case where no seats exist
        messages.warning(request, 'No seat data available')
        return redirect('red')'''