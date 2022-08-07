from django.contrib import admin
from auctions.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]

class ListingAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "seller", "current_price", "sold", "buyer"]

class BidAdmin(admin.ModelAdmin):
    list_display = ["id", "amount", "bidder", "listing", "winning"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "listing", "text"]

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Catagory)







