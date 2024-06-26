from django.shortcuts import render,redirect
from django.db import IntegrityError
from . models import Customer
from shorts.models import CreateVideo
from advertisement.models import Advertisement
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from blog.models import Blog,Comment
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import date
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import send_mail
import random, logging
from .models import Skill, UserSkill, Destination, UserDestination

# Create your views here.

def Logout(request):
    logout(request)
    return redirect('account') 

#user registration and login

@csrf_exempt
def show_account(request):
    context = {}
    if request.POST and 'register' in request.POST:
        context['register'] = True
        try:
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Generate random OTP
            num_digit = 6
            lower_bound = 10**(num_digit - 1)
            upper_bound = 10**num_digit - 1
            rnd = random.randint(lower_bound, upper_bound)
            
            # Send email with account details and OTP
            sendEmail(name, username, email, rnd)

            request.session['registration_data'] = {
                'name': name,
                'username': username,
                'email': email,
                'password': password,
                'rnd': rnd,
            }

            # Redirect to OTP verification page
            return redirect('otp_verification')
        
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            error_message = "Duplicate username or invalid input data"
            messages.error(request, error_message)
    
    elif 'login' in request.POST:
        context['register'] = False
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'account.html', context)

def sendEmail(name, username, email, rnd):
    try:
        send_mail(
            'This is a confirmation message from Travell Buddy.',  # Subject of the email
            'Hello {},\n\nYour account details:\nUsername: {}\nOTP: {}'.format(name, username, rnd),
            'your_sender_email@example.com',  # Sender's email address
            [email],  # List of recipient email addresses
            fail_silently=False,  # Set to True to suppress errors
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

def otp_verification(request):
    if request.method == 'POST':
        registration_data = request.session.get('registration_data')
        if registration_data:
            rnd = registration_data.get('rnd')
            
            # Retrieve entered OTP from form
            otp1 = request.POST.get('otp1')
            otp2 = request.POST.get('otp2')
            otp3 = request.POST.get('otp3')
            otp4 = request.POST.get('otp4')
            otp5 = request.POST.get('otp5')
            otp6 = request.POST.get('otp6')

            entered_otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6
            
            if entered_otp.isdigit() and int(entered_otp) == rnd:
                # Create user and customer accounts
                user = User.objects.create_user(
                    username=registration_data['username'],
                    password=registration_data['password'],
                    email=registration_data['email'],
                )
                customer = Customer.objects.create(
                    user=user,
                    name=registration_data['name']
                )
                messages.success(request, 'Account created successfully')
                
                # Clear session data
                del request.session['registration_data']
                
                # Redirect to more-details page with user ID
                return redirect('more-details', user.id)
            
            else:
                messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'otp_verification.html')






#more details(image,address,phone no etc)

def more_details(request, user_id):
    # if not request.user.is_authenticated or str(request.user.id) != user_id:
    # return HttpResponseForbidden("You are not allowed to access this page.")
    context = {}
    print("Inside more_details view")
    print(f"Found user: {user_id}")
    try:
        user = get_object_or_404(User, id=user_id)
        print(f"Found user: {user}")
        
        if request.method == 'POST' and 'save' in request.POST:
            print("Inside POST save block")
            image = request.FILES.get('image')
            address = request.POST.get('address')
            place = request.POST.get('location')
            pin = request.POST.get('pin')
            dob = request.POST.get('dob')

            customer, created = Customer.objects.get_or_create(user=user)

            customer.image = image
            customer.address = address
            customer.place = place
            customer.pin = pin
            customer.dob = dob


            # Save the changes
            customer.save()

            success_message = 'Additional details saved successfully'
            messages.success(request, success_message)
            sendEmailDetails(user)
            return redirect('home')

    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        error_message = "Error saving additional details"
        messages.error(request, error_message)

    return render(request, 'more-detail.html',{'user':user})


def sendEmailDetails(user):
    # Retrieve the customer's details
    try:
        customer = Customer.objects.get(user=user)
        name = customer.name
        address = customer.address
        user_email = user.email
        username = user.username
        dob = customer.dob
        place = customer.place
        pin = customer.pin

        # Send email
        send_mail(
            'Thank you for being a member of Travell Buddy.',  # Subject of the email
            'Hello {},\n\nYour account details:\nUsername: {}\nAddress: {}\nDob: {}\nPlace: {}\nPin: {}'.format(name, username, address,dob,place,pin),
            'your_sender_email@example.com',  # Sender's email address
            [user_email],  # List of recipient email addresses
            fail_silently=False,  # Set to True to suppress errors
        )
    except Customer.DoesNotExist:
        print(f"Customer details not found for user: {user.id}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e


#account update
def accountEdit(request,user_id):
    
    user = Customer.objects.get(id=user_id)
    print(user)

    if request.method == 'POST' and 'save' in request.POST:
        name = request.POST.get('name')
        username = request.POST.get('username')
        image_file = request.FILES.get('image')  # Use request.FILES
        address = request.POST.get('address')
        place = request.POST.get('location')
        pin = request.POST.get('pin')
        dob = request.POST.get('dob')

        user.name = name
        user.username = username
        if image_file:  # Check if image is provided
            user.image = 'images/user_image/'+image_file  # Assign the file to the user's image field
        user.address = address
        user.place = place
        user.pin = pin
        # user.dob = dob  # Uncomment this if you're using it

        user.save()

    
    if request.method == 'POST' and 'skill' in request.POST:
        print("skills")
        skills = request.POST.getlist('skills[]')
        user = request.user
        
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            UserSkill.objects.get_or_create(user=user, skill=skill)
        
       
    
    
    

    if request.method == 'POST' and 'destination' in request.POST:
        print("destination")
        destination = request.POST.getlist('skills[]')
        user = request.user
        
        for destination_name in destination:
            destination, created = Destination.objects.get_or_create(name=skill_name)
            UserDestination.objects.get_or_create(user=user, destination=destination)

       
    return render(request, 'account-edit.html', {'user': user})










    
    













#user account
def userAccount(request,blog_id):
   


    blog = get_object_or_404(Blog, id=blog_id)
    user = blog.owner
    user_blogs = Blog.objects.filter(owner=user)
    shorts = CreateVideo.objects.filter(owner=user)

    user_age = None
    if user.dob:
        today = date.today()
        user_age = today.year - user.dob.year - ((today.month, today.day) < (user.dob.month, user.dob.day))
   
    return render(request, 'user-account.html', {'user': user, 'blog': user_blogs, 'user_age': user_age, 'shorts': shorts})



#owner account

def ownerAccount(request,user_id):

    user = Customer.objects.get(user_id=user_id)
    blog = Blog.objects.filter(owner=user)
    shorts = CreateVideo.objects.filter(owner=user)
    advertisement = Advertisement.objects.filter(owner=user)
    # print(shorts)

    user_age = None
    if user.dob:
        today = date.today()
        user_age = today.year - user.dob.year - ((today.month, today.day) < (user.dob.month, user.dob.day))

    context = {'user': user, 'user_age': user_age, 'blog':blog,'shorts':shorts,'advertisement':advertisement}

   
    return render(request,'owner-account.html',context)

# delte account


logger = logging.getLogger(__name__)

def deleteAccount(request, user_id):
    # Ensure that the request is a POST request
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('account')
    
    logger.info(f"Starting account deletion for user_id: {user_id}")

    # Retrieve the user object
    user = get_object_or_404(User, pk=user_id)
    customer = get_object_or_404(Customer, user=user)

    try:
        # Delete related objects
        logger.info("Deleting related objects")
        Blog.objects.filter(owner__user=user).delete()
        CreateVideo.objects.filter(owner__user=user).delete()
        Comment.objects.filter(user=user).delete()
        Advertisement.objects.filter(owner=user).delete()

        # Delete the user and customer
        logger.info("Deleting customer and user")
        customer.delete()
        user.delete()

        messages.success(request, 'Account deleted successfully.')
        logger.info("Account deleted successfully")

    except Exception as e:
        logger.error(f"An error occurred while deleting the account: {e}")
        messages.error(request, f"An error occurred while deleting the account: {e}")

    # Redirect to the account page or any desired URL after deletion
    return redirect('account')