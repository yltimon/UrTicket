from .models import Member, Organizer

def member_info(request):
    # Check if the user is authenticated
    member = None
    if request.user.is_authenticated:
        member = Member.objects.filter(user=request.user).first()  # Get the member associated with the user

    return {'member': member}

def organizer_info(request):
    # Check if the organizer is authenticated
    organizer = None
    if request.user.is_authenticated:
        organizer = Organizer.objects.filter(user=request.user).first()  # Get the organizer associated with the user

    return {'organizer': organizer}