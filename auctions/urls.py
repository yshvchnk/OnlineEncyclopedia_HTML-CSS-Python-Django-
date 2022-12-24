from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing_creator, name="listing"),
    path("to_category", views.to_category, name="to_category"),
    path("item/<int:id>", views.listing_page, name="item"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("make_bid/<int:id>", views.make_bid, name="make_bid"),
    path("close_item/<int:id>", views.close_item, name="close_item"),
]
