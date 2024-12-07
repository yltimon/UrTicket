from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from collections import defaultdict
from .forms import *
from .models import *
from django.contrib import messages
from django.forms import modelformset_factory

# Create your views here.

def home(request):
    sherehe = Event.objects.all()
    return render(request, 'urticket_app/index.html', {'displaymemberevent':sherehe})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)

            # Assign the user to the appropriate model
            if user_type == 'member':
                Member.objects.create(
                    user=user,
                    fname=first_name,
                    lname=last_name,
                    phone=phone,
                    m_email=email,
                    passwd=password  # Store hashed password if needed
                )
                login(request, user)
                return redirect('home')
            elif user_type == 'organizer':
                Organizer.objects.create(
                    user=user,
                    fname=first_name,
                    lname=last_name,
                    phone=phone,
                    o_email=email,
                    passwd=password  # Store hashed password if needed
                )
                login(request, user)
                return redirect('orgdash')
    else:
        form = SignupForm()

    return render(request, 'urticket_app/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_type = form.cleaned_data.get('user_type')

            if user:
                login(request, user)

                # Redirect to dashboard based on user type
                if user_type == 'member' and hasattr(user, 'member'):
                    return redirect('home')
                elif user_type == 'organizer' and hasattr(user, 'organizer'):
                    return redirect('orgdash')
                else:
                    form.add_error(None, "Invalid user type")
        else:
            form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()

    return render(request, 'urticket_app/login.html', {'form': form})

def dash(request):
    organizer = request.user.organizer
    sherehe = Event.objects.filter(organizer=organizer)
    return render(request, 'urticket_app/organizer.html', {'display': sherehe})

def ticket(request, pk_test):
    if not request.user.is_authenticated:
        return redirect('signup')  # Redirect unauthenticated users to signup page
    
    member = get_object_or_404(Member, id=pk_test)  # Use a unique identifier for member lookup
    memberticket = OrderItem.objects.filter(order__member=member).select_related('ticket', 'ticket__event', 'order')
    
    return render(request, 'urticket_app/tickets.html', {'member': member, 'ticket': memberticket})

def ticketsbought(request, pk_org):
    organizer = get_object_or_404(Organizer, id=pk_org)
    if not request.user.is_authenticated:
        return redirect('signup')
    
    events = Event.objects.filter(organizer=organizer)
    order_items = OrderItem.objects.select_related('ticket', 'ticket__event', 'order', 'order__member').filter(ticket__event__in=events)

    # Group tickets by event
    grouped_tickets = defaultdict(list)
    grouped_tickets = {}
    for item in order_items:
        event = item.ticket.event
        if event not in grouped_tickets:
            grouped_tickets[event] = []
        grouped_tickets[event].append(item)

    return render(request, 'urticket_app/ticketsbought.html', {'grouped_tickets': grouped_tickets})

def createvent(request):
    if request.method == 'POST':
        if 'event_submit' in request.POST:  # Check for Add Event button
            event_form = AddeventForm(request.POST, request.FILES)
            if event_form.is_valid():
                event_form.save()
                return redirect('addevent')
        elif 'ticket_submit' in request.POST:  # Check for Add Ticket button
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket_form.save()  # Save the ticket
                return redirect('addevent') 
    else:
        event_form = AddeventForm()
        ticket_form = TicketForm()
    return render(request, 'urticket_app/addevent_form.html', {'form':event_form, 'ticket':ticket_form})

def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    member = request.user.member  # Assuming the logged-in user is linked to a Member
    purchase_form = TicketPurchaseForm()

    if request.method == 'POST':
        purchase_form = TicketPurchaseForm(request.POST)
        if purchase_form.is_valid():
            ticket = purchase_form.cleaned_data['ticket']
            quantity = purchase_form.cleaned_data['quantity']

            # Create the order
            order = Order.objects.create(member=member)

            # Create the order item and reduce ticket availability
            OrderItem.objects.create(order=order, ticket=ticket, quantity=quantity)
            ticket.reduce_quantity(quantity)

            messages.success(request, "Your tickets have been successfully purchased!")
            return redirect('myticket')

    return render(request, 'urticket_app/buyticket.html', {
        'event': event,
        'form': purchase_form,
    })
    
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer__user=request.user)

    if request.method == 'POST':
        form = AddeventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('orgdash')  # Redirect to the dashboard or another relevant page
    else:
        form = AddeventForm(instance=event)

    return render(request, 'urticket_app/edit_event.html', {'form': form})


def edit_tickets(request, event_id):
    # Get the event to associate tickets with
    event = get_object_or_404(Event, id=event_id, organizer__user=request.user)
    
    # Formset for managing tickets
    TicketFormSet = modelformset_factory(Ticket, fields=('name', 'price', 'qavailable'), extra=1, can_delete=True)
    ticket_queryset = Ticket.objects.filter(event=event)
    
    if request.method == 'POST':
        ticket_formset = TicketFormSet(request.POST, queryset=ticket_queryset)
        if ticket_formset.is_valid():
            tickets = ticket_formset.save(commit=False)
            for ticket in tickets:
                ticket.event = event  # Associate with the current event
                ticket.save()
            
            # Handle deleted tickets
            for ticket in ticket_formset.deleted_objects:
                ticket.delete()
            
            return redirect('edit_ticket')  # Redirect to organizer dashboard
    else:
        ticket_formset = TicketFormSet(queryset=ticket_queryset)
    
    return render(request, 'urticket_app/edit_tickets.html', {
        'ticket_formset': ticket_formset,
        'event': event
    })