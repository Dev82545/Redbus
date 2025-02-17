from django.shortcuts import render, redirect, get_object_or_404
from .models import buses, Seat_booked
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.forms import PassengerForm, SeatBookedForm, SelectPassengersForm
from home.models import Wallet, passengers
def redbus(request):
    allposts = buses.objects.all()
    context = {'allposts': allposts}
    return render(request, 'redbus.html',context)

def red(request,slug):
    bus = buses.objects.filter(slug = slug).first()
    context = {'bus':bus}
    return render(request, 'red.html', context)

@login_required
def seat(request,slug):
    f =buses.objects.filter(slug = slug).first()
    t = Seat_booked.objects.filter(buses__slug=slug, user =  request.user).first()
    g = Wallet.objects.get(user = request.user)
    if t is None:
          t = Seat_booked.objects.create(
            buses=f,
            user=request.user,
            seat_number= 0,
            lseat_number= 0,
            sseat_number= 0,
            tseat_number= 0,
        )
    '''try:'''
    query = request.GET['query']
    que = request.GET['que']
    tue = request.GET['tue']     
    query =int(query)
    que =int(que)
    tue =int(tue)
    seat = int(f.seats)
    lseat = int(f.luxury_seats)
    sseat = int(f.sleeper_seats)
    scost = int(f.seats_cost)
    lcost = int(f.sleeper_seats_cost)
    sscost = int(f.luxury_seats_cost)
    i = int(g.balance)
    '''except(KeyError, ValueError):
        messages.warning(request, 'Invalid seat selection.')
        return redirect('/')'''

    if query > seat or que > lseat or tue > sseat:
        messages.warning(request, 'Choose within the amount of seats available')
        return redirect('/')
    else: 
        total_cost = query*scost + que*lcost + tue*sscost
        if total_cost > i:
            messages.warning(request, "You do not have enough funds in your wallet. Please add funds to book tickets.")
            return redirect("wallet")
        else:
            g.balance -= total_cost
            
            t.seat_number = query
            t.lseat_number = que
            t.sseat_number = tue
            t.tseat_number = query + que + tue
            t.save()
            f.luxury_seats -= que
            f.sleeper_seats -= tue
            f.seats -= query
            
            newbalance = i - total_cost
            availableseats = {
                'regular': seat - query,
                'luxury': lseat - que,
                'sleeper': sseat - tue,
            }
            
            request.session['newbalance'] = str(newbalance)
            request.session['availableseats'] = availableseats
            messages.success(request, 'Seats selected successfully!')
            return redirect('add_passenger',booking_id=t.id)

        

def book_tickets(request):
    if request.method == 'POST':
        form = SeatBookedForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('profile')  # Define a success URL/view
    else:
        booking_form = SeatBookedForm()
        
    context = {
        'booking_form': form,
    }
    return render(request, 'book_tickets.html', context)


@login_required
def add_passenger(request, booking_id):
    # Retrieve the booking for the current user.
    booking = get_object_or_404(Seat_booked, id=booking_id, user=request.user)
    total_seats = booking.tseat_number  # total seats booked
    current_count = booking.passengers.count()
    
    # Initialize both forms.
    select_form = SelectPassengersForm()
    select_form.fields['passengers'].queryset = passengers.objects.filter(user=request.user)
    # Use consistent session key names:
    newbalance = request.session.get('newbalance')
    availableseats = request.session.get('availableseats')
    
    # Initialize passenger_form so it's always defined.
    passenger_form = PassengerForm()
    
    if request.method == "POST":
        if "select_saved" in request.POST:
            select_form = SelectPassengersForm(request.POST)
            select_form.fields['passengers'].queryset = passengers.objects.filter(user=request.user)
            if select_form.is_valid():
                saved_passengers = select_form.cleaned_data['passengers']
                for p in saved_passengers:
                    booking.passengers.add(p)
                current_count = booking.passengers.count()
                if current_count < total_seats:
                    messages.info(request, f"You have added {current_count} passenger(s). Please add {total_seats - current_count} more.")
                    return redirect('add_passenger', booking_id=booking.id)
                elif current_count == total_seats:
                    # Finalize the booking: update wallet and bus using the stored session data.
                    finalize_booking(request, booking, newbalance, availableseats)
                    messages.success(request, f"Added {saved_passengers.count()} saved passenger(s).")
                    messages.success(request, "All passenger details have been added and your booking is confirmed!")
                    return redirect('profile')
                
        elif "add_new" in request.POST:
            passenger_form = PassengerForm(request.POST)
            if passenger_form.is_valid():
                new_passenger = passenger_form.save(commit=False)
                new_passenger.user = request.user
                new_passenger.save()
                booking.passengers.add(new_passenger)
                current_count = booking.passengers.count()
                messages.success(request, "Added new passenger.")
            if current_count < total_seats:
                messages.info(request, f"You have added {current_count} passenger(s). Please add {total_seats - current_count} more.")
                return redirect('add_passenger', booking_id=booking.id)
            elif current_count == total_seats:
                # Finalize the booking: update wallet and bus using the stored session data.
                finalize_booking(request, booking, newbalance, availableseats)
                messages.success(request, "All passenger details have been added and your booking is confirmed!")
                return redirect('profile')                
    
    context = {
        "booking": booking,
        "select_form": select_form,
        "passenger_form": passenger_form,
        "current_count": current_count,
        "total_seats": total_seats,
        "new_balance": newbalance,
        "available_seats": availableseats,
    }
    return render(request, "add_passenger.html", context)

def finalize_booking(request, booking, newbalance, availableseats):
    """
    Update the wallet and bus records using the session values,
    then clear these session keys.
    """
    # Update the user's wallet.
    wallet = Wallet.objects.get(user=request.user)
    try:
        wallet.balance = int(newbalance)
    except (TypeError, ValueError):
        # If conversion fails, leave it unchanged.
        pass
    wallet.save()
    
    # Update the bus's available seats.
    bus = booking.buses
    # Use the same key names as stored in the seat view.
    bus.seats = availableseats.get('regular', bus.seats)
    bus.luxury_seats = availableseats.get('luxury', bus.luxury_seats)
    bus.sleeper_seats = availableseats.get('sleeper', bus.sleeper_seats)
    bus.save()
    
    # Clear the session keys (using the same names as stored)
    request.session.pop('newbalance', None)
    request.session.pop('availableseats', None)



