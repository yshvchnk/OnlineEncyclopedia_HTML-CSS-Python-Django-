from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def index(request):
    active_list = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listing": active_list,
        "category": categories
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


def listing_creator(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/listing.html",{
            "category": categories
        })
    else:
        title = request.POST["title"]
        descr = request.POST["descr"]
        img = request.POST["img"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user
        category_from_all = Category.objects.get(categoryTitle=category)
        bid=Bid(bid=int(price), user=user)
        bid.save()
        createListing = Listing(
            title = title,
            descr = descr,
            img = img,
            price = bid,
            category = category_from_all,
            owner = user
        )
        createListing.save()
        return HttpResponseRedirect(reverse(index))
        
def to_category(request):
    if request.method == "POST":
        cat_selected = request.POST["category"]
        category = Category.objects.get(categoryTitle=cat_selected)
        active_list = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listing": active_list,
            "category": categories
        })
        
def listing_page(request, id):
    listing_details = Listing.objects.get(pk=id)
    is_item_watch = request.user in listing_details.watchlist.all()
    comment_listing = Comment.objects.filter(listing=listing_details)
    is_owner = request.user.username == listing_details.owner.username
    return render(request, "auctions/item.html", {
        "item": listing_details,
        "is_item_watch": is_item_watch,
        "comment_listing": comment_listing,
        "is_owner": is_owner
    })
    
def remove_watchlist(request, id):
    listing_details = Listing.objects.get(pk=id)
    username = request.user
    listing_details.watchlist.remove(username)
    return HttpResponseRedirect(reverse("item", args=(id, )))

def add_watchlist(request, id):
    listing_details = Listing.objects.get(pk=id)
    username = request.user
    listing_details.watchlist.add(username)
    return HttpResponseRedirect(reverse("item", args=(id, )))

def watchlist(request):
    username=request.user
    listings = username.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
def comment(request, id):
    user = request.user
    listing_details = Listing.objects.get(pk=id)
    user_comment = request.POST['comment']
    comment = Comment(
        commentor=user,
        listing=listing_details,
        comment=user_comment
    )
    comment.save()
    return HttpResponseRedirect(reverse("item", args=(id, )))
    
def make_bid(request, id):
    bid_update = request.POST['bid']
    listing_details = Listing.objects.get(pk=id)
    is_item_watch = request.user in listing_details.watchlist.all()
    comment_listing = Comment.objects.filter(listing=listing_details)
    is_owner = request.user.username == listing_details.owner.username
    if int(bid_update) > listing_details.price.bid:
        updated_bid = Bid(user=request.user, bid=int(bid_update))
        updated_bid.save()
        listing_details.price = updated_bid
        listing_details.save()
        return render(request, "auctions/item.html", {
            "item": listing_details,
            "message": "Success bid",
            "is_item_watch": is_item_watch,
            "is_owner": is_owner,
            "comment_listing": comment_listing
        })
    else:
        return render(request, "auctions/item.html", {
            "item": listing_details,
            "message": "Unsuccess bid",
            "is_item_watch": is_item_watch,
            "is_owner": is_owner,
            "comment_listing": comment_listing
        })
        
def close_item(request, id):
    listing_details = Listing.objects.get(pk=id)
    listing_details.active = False
    listing_details.save()
    is_owner = request.user.username == listing_details.owner.username
    is_item_watch = request.user in listing_details.watchlist.all()
    comment_listing = Comment.objects.filter(listing=listing_details)
    return render(request, "auctions/item.html", {
        "item": listing_details,
        "is_item_watch": is_item_watch,
        "comment_listing": comment_listing,
        "is_owner": is_owner,
        "message": "Listing closed"
    })