from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_bids")
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} with {self.bid}"

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
        

class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startbid = models.IntegerField()
    category = models.ManyToManyField(Category, blank=True, related_name="listing_category")
    image = models.CharField(max_length=200, default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=True)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(Comments, blank=True, related_name="item_comments")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

        
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    
    def __str__(self):
        return f"{self.user.username} added {self.listing.title}"


   

