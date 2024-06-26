from django.shortcuts import render, redirect
from .forms import AdvertisementForm
from .models import Advertisement
from user.models import Customer
from django.shortcuts import get_object_or_404

def advertisement(request, user_id):
    # Retrieve the Customer object associated with the provided user_id
    print(user_id)
    user = get_object_or_404(Customer, user_id=user_id)
    
    if request.method == 'POST':
        # If the request method is POST, initialize the AdvertisementForm with the submitted data
        form = AdvertisementForm(request.POST, request.FILES)
        
        if form.is_valid():
             # If the form is valid, create a new advertisement object but do not save it yet
            advertisement = form.save(commit=False)
            # Assign the current user as the owner of the advertisement
            advertisement.owner = user
            # Save the advertisement object to the database
            advertisement.save()
            # Redirect to the home page or any other desired page upon successful form submission
            return redirect("home")
        else:
            print("Invalid form")
            print(form.errors.as_data())
    else:
        # If the request method is not POST, initialize an empty AdvertisementForm
        form = AdvertisementForm()
    
    # Render the advertisement.html template with the form
    return render(request, "advertisement.html", {'form': form})

def displayAdvertisement(request):
    return render(request,"display_advertisement.html")


def deleteAdvertisement(request,adv_id):
    advertisement =Advertisement.objects.get(id=adv_id)
    advertisement.delete()

    return render(request,"delete-advertisement.html") 