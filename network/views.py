from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
import json
from django.core.paginator import Paginator

from .models import *

now = datetime.now()


def index(request):
    allposts = (Post.objects.all().order_by("id")).reverse()
    pagesdevided = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    page_obj = pagesdevided.get_page(page_number)
    
    
    if request.user.is_authenticated:
         postslikedbyuser = request.user.liked.all()
         allpostslikedbyuser =[]
         for posts in  postslikedbyuser:
            allpostslikedbyuser.append(posts.postinaccount.id)
     
         return render(request, "network/index.html",{
        "allposts": page_obj,
        "postslikedbyuser": allpostslikedbyuser
        })
    else:
        return render(request, "network/index.html",{
        "allposts": page_obj
        })
             
        
   


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def addpost(request):
    if request.method == 'POST':
        instance = Post()
        instance.description = request.POST["description"]
        instance.likes = 0
        instance.postedby = request.user
        instance.timestamp = now
        
        instance.save()
        return HttpResponseRedirect(reverse("index"))
    
def updatecontent(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get('description')
        idofpost = data.get('id')
        instance = Post.objects.get(id = int(idofpost)) 
        instance.description = content
        instance.save() 
        return JsonResponse({'description': content})
    
    
def likeupdate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        isLiked = data.get('isLiked')
        post_id = data.get('id')

        try:
            post = Post.objects.get(id=post_id)
            current_user = request.user

            if isLiked:
                like = Likes.objects.get(postinaccount=post, likededby=current_user)
                #like.count -= 1
                #like.likededby.remove(current_user)
                #like.save()
                like.delete()
                return JsonResponse({'message': "Disliked successfully"})
                
            else:
              
                like = Likes()
                like.count = 1
                like.likededby = current_user
                like.postinaccount = post
                like.save()
                return JsonResponse({'message': "Liked successfully"})
            
        except Post.DoesNotExist:
            return JsonResponse({'message': "Post does not exist"})
        except Likes.DoesNotExist:
            return JsonResponse({'message': "Like does not exist"})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': "Invalid request method"})


def profile(request,id):
    
    #pagination
    allposts = (Post.objects.filter(postedby = id).order_by("id")).reverse()
    pagesdevided = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    page_obj = pagesdevided.get_page(page_number)
    
    
    profileof = User.objects.get(pk = id)
    follows = profileof.followers.all()
    followers = Following.objects.filter(user = profileof)
    if request.user.is_authenticated:
         postslikedbyuser = request.user.liked.all()
         allpostslikedbyuser =[]
         for posts in  postslikedbyuser:
            allpostslikedbyuser.append(posts.postinaccount.id)
         return render(request,"network/profile.html",{
        "userprofile": User.objects.get(pk = id),
        "allposts": page_obj,
        "postslikedbyuser": allpostslikedbyuser,
        "countoffollows": len(follows),
        "countoffollowers": len(followers),
        "followers": follows
    })
    else:
        return render(request, "network/index.html",{
        "allposts": page_obj
        })
        
        
        
        
def followupdate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        isfollowed = data.get('act')
        profile_id = data.get('id')

        try:
            profileof = User.objects.get(pk = profile_id)
            current_user = request.user

            if isfollowed:
                
                
                instance = Following.objects.filter(user = request.user, follows = profileof)
                instance.delete()
                return JsonResponse({'message': "Unfollowed successfully"})
                
                
            else:
                instance = Following()
                instance.user = request.user
                instance.save()
                instance.follows.add(profileof)
               
                return JsonResponse({'message': "Followed successfully"})
              
                
            
        except Post.DoesNotExist:
            return JsonResponse({'message': "Post does not exist"})
        except Likes.DoesNotExist:
            return JsonResponse({'message': "Like does not exist"})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': "Invalid request method"})
            
          
             
def followingpage(request,id):
     

     
     profileof = User.objects.get(pk = id)
     followers = Following.objects.filter(user = profileof).order_by("id")
     array=[]
     for person in followers:
         for realpeople in person.follows.all():
             for madePosts in realpeople.madepost.all():
                 array.append(madePosts)   
    
     array = array[::-1]
    #pagination
     allposts = array
     pagesdevided = Paginator(allposts, 10)
     page_number = request.GET.get('page')
     page_obj = pagesdevided.get_page(page_number)
     
     if request.user.is_authenticated:
         postslikedbyuser = request.user.liked.all()
         allpostslikedbyuser =[]
         for posts in  postslikedbyuser:
            allpostslikedbyuser.append(posts.postinaccount.id)
     
         return render(request, "network/follow.html",{
        "allposts": page_obj,
        "postslikedbyuser": allpostslikedbyuser
        })
     else:
        return render(request, "network/follow.html",{
        "allposts": page_obj
        })
    

