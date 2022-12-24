from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryTitle = models.CharField(max_length=64)
    def __str__(self):
        return self.categoryTitle

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    descr = models.CharField(max_length=2048)
    img = models.CharField(max_length=256)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    comment = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.commentor} has commented"
    
