
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addpost", views.addpost, name="addpost"),
    path("updatecontent", views.updatecontent, name="updatecontent"),
    path("updateLikes", views.likeupdate, name = "updateLikes"),
    path("<int:id>/profile", views.profile, name="profile"),
    path("updatefollows", views.followupdate, name="updatefollows"),
    path("<int:id>/followingpage", views.followingpage, name="followingpage"),
    
]
