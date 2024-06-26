from django.shortcuts import render,get_object_or_404
from user.models import Customer
from blog.models import Blog
from shorts.models import CreateVideo
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def welcome(request):
    return render(request,'welcome.html')

def Home(request):
    blogs = Blog.objects.all()
    total_likes = [blog.likes.count() for blog in blogs]
    blogs_with_likes = zip(blogs, total_likes)
    video = CreateVideo.objects.all()
    return render(request, "home.html", {'blogs_with_likes': blogs_with_likes, 'video': video})



# @login_required
def blogDetails(request,user_id):
    blog = Blog.objects.get(id=user_id)
    # user = Customer.objects.get(id=user_id)
    return render(request,"bbb.html",{'blog':blog})



def search_blog(request):
    query = request.GET.get('q')
    
    # Filter blogs based on search query
    if query:
        blogs = Blog.objects.filter(
            Q(location__icontains=query) |
            Q(owner__user__username__icontains=query) |
            Q(author__icontains=query) |
            Q(header__icontains=query) |  # Added heading field
            Q(title__icontains=query)       # Added title field 
        )
    else:
        blogs = Blog.objects.none()  # Return an empty queryset if no query is provided
    
    return render(request, 'search_results.html', {'blogs': blogs, 'query': query})



def travellBuddyPage(request):
    return render(request,"travell_buddy_page.html")

