from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed", views.closed, name="closed")
]
