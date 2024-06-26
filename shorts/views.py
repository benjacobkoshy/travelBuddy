from django.shortcuts import render,redirect
from .forms import CreateVideoForm
from .models import CreateVideo
from user.models import Customer

# Create your views here.

def shortVideo(request):
    video = CreateVideo.objects.all()
    return render(request,"short-video.html",{'video':video})

def createVideo(request, user_id):
    if request.method == 'POST':
        form = CreateVideoForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the user object using the user ID
            user = Customer.objects.get(user_id=user_id)
            # Save the video instance along with the user
            video = form.save(commit=False)
            video.owner = user
            video.save()
            return redirect('short-video')  # Redirect to success page
    else:
        form = CreateVideoForm()
    return render(request, 'create-video.html', {'form': form})


def deleteShorts(request,video_id):
    shorts = CreateVideo.objects.get(id=video_id)
    shorts.delete()

    return render(request,"delete_blog.html")  