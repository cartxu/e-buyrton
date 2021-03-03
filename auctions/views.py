from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *


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


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False)
    })

#Página que muestra las subastas ya cerradas

def closed(request):
    return render(request, "auctions/closed.html", {
        "listings": Listing.objects.filter(closed=True)
    })

# ESTA FUNCIÓN MUESTRA TODAS LAS CATEGORÍAS EXISTENTES
def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html",{
        "categories": categories
    })
# ESTA FUNCIÓN FILTRA LAS SUBASTAS POR CATEGORÍA:
def category(request, category_id): 
    category = Category.objects.get(id=category_id)
    listing = Listing.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "category": category,
        "categories": listing
    })

# CREAR NUEVA SUBASTA (SOLO USUARIOS)
@login_required(login_url="/login")
def create_listing(request):

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/create.html",{
                "form": form
                
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm
        })

# PAGINA PARA PUBLICAR COMENTARIOS (SOLO USUARIOS):
@login_required(login_url="/login")
def comment(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(id=listing_id)

    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            return render(request, "auctions/comment.html", {
                "form": form,
                "listing": listing,
                "listing_id": listing.id,
            })
    else:
        return render(request, "auctions/comment.html", {
            "form": CommentsForm(),
            "listing": listing,
            "listing_id": listing.id
        })


# Mostrar página Watchlist del usuario
@login_required(login_url="/login")
def watchlist(request):
    user = User.objects.get(username=request.user)
    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlist": watchlist
    })


# PÁGINA DETALLADA DE SUBASTA CON INFO, PUJAS, COMENTARIOS...
# En esta página el usuario verá toda la info del artículo y sus comentarios.
# Si está registrado podrá pujar por el artículo y podrá comentar, añadir/eliminar de su watchlist.
# Si el usuario es el autor de la subasta podrá cerrarla.
# Si la subasta está cerrada y el usuario ha ganado, deberá verlo.
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comments
    
    
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        #si el usuario online no es el mismo que publicó la subasta
        if user.username != listing.user.username:
            
            if request.method == "POST" and request.POST.get("watchlist"):  #agrega listing a su watchlist
                
                #Chequeamos si el usuario no tiene este listing en su watchlist
                if user.watchlist.filter(listing=listing).exists():
                    user.watchlist.filter(listing=listing).delete()
                    return render(request, "auctions/listing.html", {
                        "listing" : listing,
                        "fav": "Deleted from Watchlist!",
                        "form": BidForm
                        }) 
                else:
                    watchlist = Watchlist()
                    watchlist.user = user
                    watchlist.listing = listing
                    watchlist.save()
                    return render(request, "auctions/listing.html", {
                        "listing" : listing,
                        "fav": "Added to Watchlist!",
                        "form": BidForm
                        }) 
                return render(request, "auctions/listing.html", {
                        "listing" : listing,
                        "form": BidForm
                        }) 

            elif request.method == "POST" and request.POST.get("bid"):
                
                form = BidForm(request.POST)

                if form.is_valid():
                    bid = int(request.POST["bid"])
                    price = listing.startbid
                    
                    if bid > price: 
                        bid = form.save(commit=False)
                        bid.user = request.user
                        bid.save()
                        listing.startbid = int(request.POST["bid"])
                        listing.bids.add(bid)
                        listing.save()

                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "form": BidForm,
                            "message": "Your bid was successfully posted!"
                        })

                    else:
                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "form": BidForm,
                            "message": "Your bid must be greater than the current price."
                        }) 
        
                else: 
                    return render(request, "auctions/listing.html", {
                        "listing" : listing,
                        "form": BidForm,
                        "message": "Please, enter a valid amount."
                    })     
        else:
            if listing.closed is False:
                if request.method == "POST" and request.POST.get("close"):
                    listing.closed = True
                    listing.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
            else:
                if request.method == "POST" and request.POST.get("open"):
                    listing.closed = False
                    listing.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing.id,)))

                return render(request,"auctions/listing.html", {
                        "listing" : listing,
                        "form": BidForm,
                        "comments": comments
                    })
            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "form": BidForm,
                "comments": comments
                
                })  

        return render(request, "auctions/listing.html", {
                "listing" : listing,
                "form": BidForm,
                "comments": comments
                
                })  

    else:
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "comments": comments
                       
        })
        
    
