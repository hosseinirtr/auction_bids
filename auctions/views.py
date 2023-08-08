from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import User, Categories, Listing
from .models import User, WatchlistItem, Comment


def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html", {
        'listing': activeListing,
        'categories': Categories.objects.all()
    })


def details(request, id):
    user = request.user
    details_item = Listing.objects.get(id=id)
    listing = get_object_or_404(Listing, pk=id)
    iswatchlisted = WatchlistItem.objects.filter(
        user=user, listing=listing).exists()
    img_path = 'http://' + request.get_host() + '/media/' + \
        str(details_item.imageUrl)
    return render(request, 'auctions/details.html', {
        'body': details_item, 'title': details_item.title, "img_path": img_path, "isWatchlist": iswatchlisted
    })


@login_required
def addWatchlist(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    Watchlist_Item = WatchlistItem.objects.create(user=user, listing=listing)
    Watchlist_Item.save()
    # Redirect to the listing detail page or a desired URL
    return HttpResponseRedirect(reverse('details', args=[id, ]))


@login_required
def removeWatchlist(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    watchlist_item = WatchlistItem.objects.filter(
        user=user, listing=listing).first()
    watchlist_item.delete()
    # Redirect to the listing detail page or a desired URL
    return HttpResponseRedirect(reverse('details', args=[id, ]))


def displayCategories(request):

    img_path = 'http://' + request.get_host() + '/media/'
    allCategory = Categories.objects.all()
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Categories.objects.get(categoryName=categoryFromForm)
        activeListing = Listing.objects.filter(
            isActive=True, category=category)
        return render(request, 'auctions/displayCategories.html', {
            'listing': activeListing,
            'categories': allCategory
        })
    else:
        return render(request, 'auctions/displayCategories.html', {
            'categories': allCategory,
            'imgPathBase': img_path
        })


def create_listing(request):
    if (request.method == "GET"):
        all_categories = Categories.objects.all()
        return render(request, 'auctions/create.html',
                      {
                          'categories': all_categories
                      })
    if (request.method == "POST"):
        print(request.POST, request.method)
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        imageFile = request.FILES["imageFile"]
        category_name = request.POST["category"]
        category = Categories.objects.get(categoryName=category_name)
        this_user = request.user
        new_item = Listing(title=title, description=description,
                           price=price, imageUrl=imageFile, owner=this_user,
                           category=category
                           )
        new_item.save()
        return HttpResponseRedirect(reverse('index'))


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


def addComment(request, listing_id):
    if request.method == "POST":
        message = request.POST['message']
        author = request.user
        add_comment = Comment.objects.create(
            author=author, listing_id=listing_id, message=message)
        add_comment.save()
        return HttpResponseRedirect(reverse('details', args=[listing_id, ]))
