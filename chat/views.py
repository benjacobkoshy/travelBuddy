from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from user.models import Customer
from django.http import HttpResponse
from django.db import IntegrityError


from django.db.models import Q

@login_required
def send_message(request, receiver_id):
    sender = request.user.customer_profile
    receiver = Customer.objects.get(id=receiver_id)
    
    # Retrieve messages and order them by timestamp in ascending order
    messages = Message.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('chat')
        if content:
            # Create a new message
            Message.objects.create(sender=sender, receiver=receiver, content=content)
            # Refresh the messages queryset after adding the new message
            messages = Message.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    
    return render(request, 'send_message.html', {'receiver': receiver, 'messages': messages})




@login_required


def inbox(request, user_id):
    try:
        main_user = Customer.objects.get(user_id=user_id)
        messages_sent = Message.objects.filter(sender=main_user)
        messages_received = Message.objects.filter(receiver=main_user)

        # Combine sent and received messages
        messages = messages_sent | messages_received

        user_ids = set()

        # Extract user IDs from messages
        for message in messages:
            # Add sender's ID
            user_ids.add(message.sender.user_id)
            # Add receiver's ID
            user_ids.add(message.receiver.user_id)

        # Remove main user's ID from the set if it exists
        if main_user.user_id in user_ids:
            user_ids.remove(main_user.user_id)

        # Retrieve users who the main user has interacted with
        users_interacted = Customer.objects.filter(user_id__in=user_ids)
    except Customer.DoesNotExist:
        error_message = "User does not exist."
        messages.error(request, error_message)
        users_interacted = None
    except IntegrityError as e:
        error_message = f"IntegrityError: {e}"
        messages.error(request, error_message)
        users_interacted = None

    return render(request, "chat_main.html", {"users_interacted": users_interacted})


def searchUser(request):
    query = request.GET.get('query')
    print('query')

    if query:
        users = Customer.objects.filter(
             Q(user__username__icontains=query) | 
             Q(name__icontains=query)
        )
    else:
        users = Customer.objects.none()
    print("hi")
    print(users)

    return render(request, "chat_main.html", {'users': users, 'query': query})
