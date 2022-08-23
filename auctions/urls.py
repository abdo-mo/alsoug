from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active_listings", views.active_listings, name="active_listings"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment", views.comment, name="comment"), 
    path("catagories", views.catagories, name="catagories"),
    path("<int:catagory_id>", views.catagory, name="catagory")
]
