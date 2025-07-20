from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
import re
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(request):

    return render(request,'index.html')

def user_reg(request):
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST['password']
        if login_tbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:
            log=login_tbl.objects.create_user(username=email,password=password,usertype='user',is_active=1)
            log.save()
            user=Users(name=name,email=email,phone=phone,address=address,user=log)
            user.save()
            messages.success(request,'User Registered Successfully')

    return render(request,'user_reg.html')

def club_reg(request):
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST['password']
        image=request.FILES['image']
        description=request.POST['description']
        if login_tbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:
            log=login_tbl.objects.create_user(username=email,password=password,usertype='club',is_active=0)
            log.save()
            club=Clubs(name=name,email=email,phone=phone,address=address,image=image,description=description,user=log)
            club.save()
            messages.success(request,'Club Registered Successfully')

    return render(request,'club_reg.html')

def user_login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(username=email,password=password)
        if user is None:
            messages.info(request,"Invalid username or admins approval pending")
        else:
            auth_login(request,user)
            if user.is_superuser:
                return redirect('/adminhome')
            elif user.usertype=='user' and user.is_active==1:
                r=Users.objects.get(email=email)
                request.session['id']=r.id
                return redirect('/userhome')
            elif user.usertype=='club' and user.is_active==1:
                r=Clubs.objects.get(email=email)
                request.session['id']=r.id
                return redirect('/clubhome')
            else:
                messages.info(request,'Your account is not approved by admin')
    return render(request,'login.html')
@login_required
def adminhome(request):
    return render(request,'adminhome.html')

@login_required
def userhome(request):
    return render(request,'userhome.html')

@login_required
def clubhome(request):
    return render(request,'clubhome.html')

#i want to update name,email,phone,address,password

@login_required
def user_profile_update(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']

        # Validate inputs
        if not re.match(r"[A-Za-z\s]+$", name):
            messages.error(request, "Name can only contain alphabets.")
            return redirect('user_profile_update')
        if not re.match(r"[6789][0-9]{9}", phone):
            messages.error(request, "Invalid phone number.")
            return redirect('user_profile_update')

        try:
            # Fetch user and login objects
            user = Users.objects.get(id=request.session['id'])
            log = login_tbl.objects.get(username=user.email)

            # Update user details
            user.name = name
            user.email = email
            user.phone = phone
            user.address = address
            user.save()

            # Update login details
            log.username = email
            if password.strip():  # Update password only if provided
                log.set_password(password)
            log.save()

            messages.success(request, "Profile Updated Successfully")
        except Users.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login')
        except login_tbl.DoesNotExist:
            messages.error(request, "Login record does not exist.")
            return redirect('login')

    # Render the update profile page
    user = Users.objects.get(id=request.session['id'])
    return render(request, 'user_profile_update.html', {"data": user})


@login_required
def club_profile_update(request):
    cid=request.session['id']
    club=Clubs.objects.get(id=cid)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        description = request.POST.get('description', '').strip()
        password = request.POST.get('password', '').strip()

        # Validate inputs
        if not re.match(r"^[A-Za-z\s]+$", name):
            messages.error(request, "Name should contain only alphabets and spaces.")
            return redirect('club_profile_update')
        if not re.match(r"^[6789]\d{9}$", phone):
            messages.error(request, "Invalid phone number.")
            return redirect('club_profile_update')

        try:
            # Fetch club and login_tbl objects
            club = Clubs.objects.get(id=cid)  # Assuming `request.user` is linked to the login_tbl
            login_record = login_tbl.objects.get(username=club.email)

            # Update club details
            club.name = name
            club.email = email
            club.phone = phone
            club.address = address
            club.description = description
            club.save()

            # Update password if provided
            login_record.username = email
            if password:
                login_record.set_password(password)
            login_record.save()

            # Save highlight images
            if 'highlights' in request.FILES:
                images = request.FILES.getlist('highlights')
                for image in images:
                    Club_Highlights.objects.create(club=club, image=image)

            messages.success(request, "Profile updated successfully!")
            return redirect('club_profile_update')
        except Clubs.DoesNotExist:
            messages.error(request, "Club not found.")
            return redirect('login')
        except login_tbl.DoesNotExist:
            messages.error(request, "Login record not found.")
            return redirect('login')

    # Fetch current club details and highlights to display in the form
    try:
        club = Clubs.objects.get(id=cid)
        highlights = Club_Highlights.objects.filter(club=club)
        return render(request, 'club_profile_update.html', {'data': club, 'highlights': highlights})
    except Clubs.DoesNotExist:
        messages.error(request, "Club not found.")
        return redirect('login')
    



from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Clubs, Events
@login_required
def club_add_event(request):
    if request.method == "POST":
        try:
            club = Clubs.objects.get(id=request.session['id'])
            
            name = request.POST['name']
            event_datetime = request.POST['event_datetime']
            description = request.POST['description']
            address = request.POST['address']
            capacity = request.POST['capacity']
            price = request.POST['price']
            vip_price = request.POST.get('vip_price')
            vip_capacity = request.POST.get('vip_capacity')
            main_image = request.FILES.get('main_image')
            artist = request.POST['artist']
            event_category = request.POST['category']
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            date = datetime.now()

            event_datetime_obj = datetime.strptime(event_datetime, '%Y-%m-%dT%H:%M')
            if event_datetime_obj < datetime.now():
                messages.error(request, "Event date and time cannot be in the past.")
                return redirect('club_add_event')

            # Create event with location
            event = Events.objects.create(
                club=club,
                name=name,
                event_at=event_datetime_obj,
                description=description,
                address=address,
                capacity=capacity,
                price=price,
                created_at=date,
                vip_price=vip_price if vip_price else None,
                vip_capacity=vip_capacity if vip_capacity else None,
                main_image=main_image,
                artist=artist,
                event_category=event_category,
                lattitude=latitude,
                longitude=longitude
            )
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('club_add_event')
        except Clubs.DoesNotExist:
            messages.error(request, "You must be associated with a club to add events.")
            return redirect('club_dashboard')

    club_events = Events.objects.filter(club_id=request.session['id']).order_by('-event_at')
    return render(request, 'club_add_event.html', {"events": club_events})



from django.shortcuts import render
from django.db.models import Q, F, ExpressionWrapper, FloatField
from django.utils.timezone import now
from django.db.models.functions import Power, Sqrt
from .models import Events
from geopy.distance import geodesic
@login_required
def view_and_book_events(request):
    events = Events.objects.filter(event_at__gte=now()).order_by('event_at')

    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    filter_nearest = request.GET.get('nearest')
    user_lat = request.GET.get('user_lat')
    user_lon = request.GET.get('user_lon')

    # Apply search filters
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(event_category__icontains=search_query) |
            Q(artist__icontains=search_query)
        )

    # Apply date filter
    if start_date and end_date:
        events = events.filter(event_at__date__range=[start_date, end_date])

    # Apply ticket price filter
    if min_price and max_price:
        events = events.filter(price__range=[min_price, max_price])

    

    # Filter by nearest events within 1 km
    if filter_nearest and user_lat and user_lon:
        user_location = (float(user_lat), float(user_lon))
        filtered_events = []

        for event in events:
            event_location = (event.lattitude, event.longitude)
            distance_km = geodesic(user_location, event_location).kilometers

            if distance_km <= 5:  # Filter events within 1 km
                filtered_events.append(event)

        events = filtered_events  # Update the events list
       
    return render(request, 'view_and_book_events.html', {'events': events})




from django.utils.timezone import now


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Events
@login_required
def payment(request):
    if request.method == "POST":
        try:
            # Fetch data from the booking form
            event_id = request.POST.get('event_id')

            # Ensure empty fields default to 0
            nquantity = request.POST.get('nquantity', '0').strip()
            vquantity = request.POST.get('vquantity', '0').strip()

            nquantity = int(nquantity) if nquantity.isdigit() else 0
            vquantity = int(vquantity) if vquantity.isdigit() else 0

            # Get the user and event objects
            user_id = request.session.get('id')
            if not user_id:
                messages.error(request, "Session expired. Please log in again.")
                return redirect('login')

            user = Users.objects.get(id=user_id)
            event = Events.objects.get(id=int(event_id))

            # Check if at least one type of ticket is selected
            if nquantity == 0 and vquantity == 0:
                messages.error(request, "Please select at least one ticket.")
                return redirect('view_and_book_events')

            # Check availability of normal tickets
            if nquantity > event.capacity:
                messages.error(request, f"Only {event.capacity} normal tickets available.")
                return redirect('view_and_book_events')

            # Check availability of VIP tickets (handle None case)
            if event.vip_capacity is not None and vquantity > event.vip_capacity:
                messages.error(request, f"Only {event.vip_capacity} VIP tickets available.")
                return redirect('view_and_book_events')

            # Calculate total price
            total_price = (nquantity * event.price) + (vquantity * (event.vip_price or 0))

            # Pass data to the payment page
            context = {
                'user': user,
                'event': event,
                'nquantity': nquantity,
                'vquantity': vquantity,
                'total': total_price,
            }
            return render(request, 'cus_pay.html', context)

        except Events.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('view_and_book_events')
        except Users.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')
        except ValueError:
            messages.error(request, "Invalid data provided. Please enter a valid number of tickets.")
            return redirect('view_and_book_events')
    else:
        return redirect('view_and_book_events')


    
@login_required
def confirm_booking(request):
    if request.method == "POST":
        try:
            # Retrieve data from the payment form
            event_id = request.POST.get('event_id')
            nquantity = int(request.POST.get('nquantity', 0))
            vquantity = int(request.POST.get('vquantity', 0))
            user = Users.objects.get(id=request.session['id'])
            event = Events.objects.get(id=event_id)

            # Update ticket availability
            if nquantity > event.capacity:
                messages.error(request, "Not enough normal tickets available.")
                return redirect('view_and_book_events')

            if vquantity > event.vip_capacity and event.vip_capacity is not None:
                messages.error(request, "Not enough VIP tickets available.")
                return redirect('view_and_book_events')

            event.capacity -= nquantity
            if event.vip_capacity is not None:
                event.vip_capacity -= vquantity
            event.save()

            # Create a booking record
            booking = Booking(
                user=user,
                event=event,
                nquantity=nquantity,
                vquantity=vquantity,
                status='confirmed',
                created_at=now()
            )
            booking.save()

            messages.success(request, "Payment successful! Booking confirmed.")
            return redirect('view_and_book_events')

        except Events.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('view_and_book_events')
        except Users.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')
    else:
        return redirect('view_and_book_events')
    
from django.core.paginator import Paginator

@login_required
def booking_history(request):
    # Check if user is logged in
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view your booking history.")
        return redirect('login')  # Replace 'login' with your login view name

    try:
        user = Users.objects.get(id=request.session['id'])
        # Fetch user's bookings and related event details
        bookings = Booking.objects.filter(user=user).select_related('event').order_by('-created_at')

        # Pagination
        paginator = Paginator(bookings, 5)  # Display 5 bookings per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'booking_history.html', {
            'page_obj': page_obj,
            'bookings': page_obj.object_list,  # List of bookings for the current page
            'now': now(),  # Pass the current datetime for template checks
        })
    except Users.DoesNotExist:
        messages.error(request, "Invalid user session. Please log in again.")
        return redirect('login')
@login_required
def cancel_booking(request, booking_id):
    # Handle booking cancellation logic
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to cancel a booking.")
        return redirect('login')

    try:
        user = Users.objects.get(id=request.session['id'])
        booking = get_object_or_404(Booking, id=booking_id, user=user)

        # Prevent cancellation of past events
        if booking.event.event_at < now():
            messages.error(request, "Cannot cancel a booking for a past event.")
            return redirect('booking_history')

        # Prevent cancelling an already cancelled booking
        if booking.status == "Cancelled":
            messages.warning(request, "This booking is already cancelled.")
            return redirect('booking_history')

        # Update event capacity and booking status
        event = booking.event
        event.capacity += booking.nquantity or 0
        event.vip_capacity += booking.vquantity or 0
        event.save()

        booking.status = "Cancelled"
        booking.save()

        
        return redirect('booking_history')

    except Users.DoesNotExist:
        messages.error(request, "Invalid user session. Please log in again.")
        return redirect('login')

@login_required
def admin_user_management(request):
    users = Users.objects.all()  # Fetch all users

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        if user_id and action:
            user = get_object_or_404(Users, id=user_id)

            if action == "approve":
                user.user.is_active = 1  # Activate the associated login_tbl user
                user.user.save()  # Save the login_tbl instance
                messages.success(request, f"{user.name} has been approved.")
            elif action == "reject":
                user.user.is_active = False  # Deactivate the associated login_tbl user
                user.user.save()  # Save the login_tbl instance
                messages.error(request, f"{user.name} has been rejected.")

        else:
            messages.error(request, "Invalid user ID or action.")

        return redirect('admin_user_management')

    return render(request, 'admin_user_management.html', {'users': users})

@login_required
def admin_club_management(request):
    # Fetch all clubs to display
    clubs = Clubs.objects.all()

    if request.method == "POST":
        club_id = request.POST.get("club_id")
        action = request.POST.get("action")
        club = get_object_or_404(Clubs, id=club_id)
        
        # Perform actions based on approval or rejection
        if action == "approve":
            if hasattr(club.user, 'is_active'):
                club.user.is_active = True  # Activate the club user
                club.user.save()
                messages.success(request, f"{club.name} has been approved and activated.")
        elif action == "reject":
            if hasattr(club.user, 'is_active'):
                club.user.is_active = False  # Deactivate the club user
                club.user.save()
                messages.error(request, f"{club.name} has been rejected and deactivated.")

        return redirect('admin_club_management')  # Redirect back to the management page

    return render(request, 'admin_club_management.html', {'clubs': clubs})



@login_required
def admin_booking_overview(request):
    

    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'admin_booking_review.html', {'bookings': bookings})

def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('login')


