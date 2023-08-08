from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path('categories', views.displayCategories, name="displayCategories"),
    path('watchlists', views.displaywatchlists, name="displaywatchlists"),
    path("details/<str:id>", views.details, name="details"),
    path("addComment/<str:id>", views.addComment, name="addComment"),
    path("addBid/<str:id>", views.addBid, name="addBid"),
    path("addWatchlist/<str:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<str:id>", views.removeWatchlist, name="removeWatchlist"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
