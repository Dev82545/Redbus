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
    query =int(query)
    seat = int(f.seats)
    if seat == 0:  # ✅ Handle case where no seats exist
        #messages.warning(request, 'No seat data available')
        return HttpResponse('Hello1')
    if query > seat:
        #messages.warning(request, 'Choose the amount of seats available')
        return HttpResponse('Hello')
    else:
        f.seats -= query
        f.save()
        messages.success(request, 'Seats selected successfully!')
        return redirect('seat')


