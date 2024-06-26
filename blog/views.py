from django.shortcuts import render,redirect,get_object_or_404
from .models import Blog,Comment
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from user.models import Customer
from django.http import HttpResponseRedirect
from django.urls import reverse
from user.models import Customer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
# create blog
def create_blog(request, user_id):
   
    user = get_object_or_404(User, id=user_id)
    print("Inside more_details view")
    print(f"Found user: {user_id}")
    if request.POST and 'publish' in request.POST:
        try:
            new_blog = Blog.objects.create(
                        header=request.POST['header'],
                        title=request.POST['title'],
                        date=request.POST['date'],
                        location=request.POST['location'],
                        content=request.POST['content'],
                        image=request.FILES.get('image'),
                        # video=request.FILES.get('video'),
                        owner=user.customer_profile,  # Assuming Customer model has a OneToOneField to User
                        author=request.POST['author'],
                        yourself=request.POST['yourself']
                    )

            return redirect("home")  # Redirect to the same page after successful submission
        except Exception as e:
            print(f"IntegrityError: {e}")
            error_message = "Duplicate username or invalid input data"
            messages.error(request,error_message)
    return render(request, "create-blog.html",{'user':user})



@login_required
def LikeView(request, pk):
    if request.user.is_authenticated:
          
        if request.method == 'POST':
            blog = get_object_or_404(Blog, id=pk)
            customer_instance = request.user.customer_profile
            
            if customer_instance in blog.likes.all():
                # User already liked the blog, so remove the like
                blog.likes.remove(customer_instance)
                liked = False
            else:
                # User hasn't liked the blog, so add the like
                blog.likes.add(customer_instance)
                liked = True
            
            return HttpResponseRedirect(reverse('home'))
    else:
        # If it's not a POST request, redirect to the account page
       return HttpResponseRedirect("account")


#comments
@login_required
def Comments(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, pk=blog_id)
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(blog=blog, user=request.user, text=comment_text)
    
    blog = get_object_or_404(Blog, pk=blog_id)
    
    # Get all comments related to the retrieved blog object
    comments = Comment.objects.filter(blog=blog)
    return render(request, 'comments.html', {'blog': blog, 'comments': comments})

#delete blog
def deleteBlog(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()

    return render(request,"delete_blog.html")


#bookmark

def add_to_bookmark(request, blog_id):
    return render(request,'bookmark.html')

    
   


