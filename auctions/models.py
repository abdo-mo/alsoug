from django.contrib.auth.models import AbstractUser
from django.db import models
from sqlalchemy import null
from datetime import datetime

class Catagory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", null=True ,blank=True, related_name="users")

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_listings")
    current_price = models.FloatField()
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="bought_listings")
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, related_name="listings", null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="staticfiles/auctions/images", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
 

class Bid(models.Model):
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    winning = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.amount}$"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"


