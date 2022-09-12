from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.test import modify_settings
from django.urls import reverse
from auctions.utils import *
from django.contrib.auth.decorators import login_required
from django import forms

from .models import *

class UploadImageForm(forms.Form):
    image = forms.ImageField()


def index(request):
    featured_listings = Listing.objects.filter(featured=True)
    return render(request, "auctions/index.html", {
        "featured_listings": featured_listings
    })

def active_listings(request):
    listings = Listing.objects.filter(sold=False)
    listings.order_by("created_time")
    return render(request, "auctions/active_listings.html", {
        "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    catagories = Catagory.objects.all()

    if request.method == "POST":

        # Check if a hacker messed the names of the inputs
        try:
            title = request.POST["title"]
            print(f'Assigning title is done successfully VALUE={title}')

            description = request.POST["description"]
            print(f'Assigning description is done successfully VALUE={description}')


            image = request.FILES["image"]
            print(f'Assigning image is done successfully VALUE={image}')

            starting_bid = request.POST["starting_bid"]
            print(f'Assigning starting_bid is done successfully VALUE={starting_bid}')

            catagory = request.POST["catagory"]



        except:
            return render(request, "auctions/new_listing.html", {
                "catagories": catagories, 
                "alert": "<div style='padding: 20px 20px ' class='red-alert'> Some information is missing, Please fill all the empty fields!</div>"
            })
        

        # validate listing
        valid_listing = validate_new_listing(title, description, image, starting_bid, request.POST["catagory"])
        
        if valid_listing:
            catagory = Catagory.objects.get(name=request.POST["catagory"])
            listing = Listing(seller=request.user, title=title, description=description, image=image, current_price=float(starting_bid), catagory=catagory)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                "catagories": catagories, 
                "alert": "<h2>Invalid input</h2>"
            })


    return render(request, "auctions/new_listing.html", {
        "catagories": catagories
    })

""" ON PROGRESS VIEW """
@login_required
def listing(request, listing_id):    
    listing = Listing.objects.get(pk=listing_id)
    watchlist = request.user.watchlist.all()
    comments = listing.comments.all()
    comments.order_by("created_time")

    """ 
    Before the complexity starts, you should know these thigns:
    1. 
    
    """

    # POST
    if request.method == "POST":

        # If the user is NOT the seller of the listing

        if request.user != listing.seller:
            # check existence of input
            try:
                amount = float(request.POST["amount"])
            except:
                return render(request, "auctions/error.html", {
                    "message": "Invalid Bid: you type a non-float thing"
                })


            # Check if the bid is valid
            if validate_bid(amount, listing):

                if Bid.objects.filter(winning=True).first():
                    winning_bids = Bid.objects.filter(winning=True)
                    for winning_bid in winning_bids:
                        winning_bid.winning = False     
                        winning_bid.save()               

                # UPDATE Bids
                bid = Bid(amount=amount, bidder=request.user, listing=listing, winning=True)
                bid.save()

                # UPDATE Listings
                listing.current_price = amount
                listing.buyer = request.user
                listing.save()


                alert = '<div class="green-alert">You Made a Bid Successfully!</div>'

                return render(request, "auctions/listing.html", {
                    "alert": alert,
                    "listing": listing,
                    "watchlist": watchlist, 
                    "comments": comments
                })

            else:
                alert = '<div class="red-alert"> Invalid Bid: The bidded amount is less than or equal the current price of the listing. To make a successful bid on the this listing, make a bid with an amount of money that is higher than the current price of the listing. </div>'
                return render(request, "auctions/listing.html", {
                    "watchlist": watchlist,
                    "alert": alert,
                    "listing": listing,
                    "comments": comments
                })

        # If the user is the seller of the listing
        else:
            # security tests
            try:
                close = request.POST["close"]
            except:
                return render(request, "auctions/error.html", {
                    "message": " you messed with html form, the police is on the way"
                })
            
            # Validate form
            if not validate_close(close):
                return render(request, "auctions/error.html", {
                    "message": " you messed with html CLOSE AUCTION form, the police is on the way"
                })

            # Check if there are bids on the listings
            if Bid.objects.filter(listing=listing).first():
                # Close the auction
                listing.sold = True
                listing.save()
                alert = f'<div class="green-alert">You closed the auctions for this listing successfully and sold the listing at the price of {listing.current_price}$ to {listing.buyer}</div>'
                return render(request, "auctions/listing.html", {
                    "alert": alert,
                    "listing": listing,
                    "comments": comments
                })

            else:
                alert = '<div class="red-alert" role="alert"> There are no bids yet on this listing, you can not close it now!</div>'
                return render(request, "auctions/listing.html", {
                    "alert": alert,
                    "listing": listing,
                    "comments": comments
                })
            
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments
    })


@login_required
def watchlist(request):
    if request.method == "POST":

        # Validate form names
        try:
            listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
            operation = request.POST["modify"]
        except:
            return render(request, "auctions/error.html", {
                "message": "SO, YOU ARE TRYING TO MESS WITH THE FORM HUH? WELL, THE POLICE IS ON THE WAY!"
            })
        
        # After making sure the form values are okay
        # Let's validate the input

        if validate_operation(operation):
            if operation == "add":
                request.user.watchlist.add(listing)
                request.user.save()
            else:
                request.user.watchlist.remove(listing)
                request.user.save()
            return HttpResponseRedirect(reverse("watchlist"))
        return render(request, "auctions/error.html", {
            "message": "Invalid operation"
        })
    
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


def comment(request):
    if request.method == "POST":
        try:
            text = request.POST["comment"]
            listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        except:
            return render(request, "auctions/error.html", {
                "message": "You messed up the comment form! The Police is on the way!"
            })

        user = request.user
        
        if valid_comment(text):
            # Saving the comment
            comment = Comment(user=user, listing=listing, text=text)
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "alert": '<div class="alert alert-danger" role="alert"> You can not post an empty comment </div>',
            "watchlist": user.watchlist.all(),
            "comments": listing.comments.all()
        })


def catagories(request):
    catagories = Catagory.objects.all()
    catagories.order_by("name")
    return render(request, "auctions/catagories.html", {
        "catagories": catagories
    })


def catagory(request, catagory_id):
    catagory = Catagory.objects.get(pk=catagory_id)
    listings = Listing.objects.filter(catagory=catagory, sold=False)
    listings.order_by("-created_time")
    
    # You left here
    return render(request, "auctions/catagory.html", {
        "listings": listings,
        "catagory": catagory
    })


