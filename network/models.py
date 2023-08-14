from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
     

class Post(models.Model):
    description = models.TextField(max_length=1000)
    postedby = models.ForeignKey(User,on_delete=models.CASCADE,related_name="madepost",blank=True,null=True)
    timestamp = models.DateTimeField(blank=True,null=True)
    likes = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.description} posted by {self.postedby} on {self.timestamp}"
    
    
class Likes(models.Model):
    count = models.IntegerField(default = 0, blank=True,null=True)
    postinaccount = models.ForeignKey(Post,on_delete=models.PROTECT,related_name="havelikes",blank=True,null=True)  
    likededby = models.ForeignKey(User,on_delete=models.PROTECT,related_name="liked",blank=True,null=True)
    def __str__(self):
        return f"{self.likededby} liked on {self.postinaccount}"
    
    
class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name="user",blank=True,null=True)
    follows = models.ManyToManyField(User,blank=True,null=True,related_name="followers")  
    def __str__(self):
        return f"{self.user} follows {self.follows.all()}" 
    
