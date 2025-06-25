from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")
# The following viewsets will be added back later
# router.register(r'authors', views.AuthorViewSet, basename='author')
# router.register(r'publishers', views.PublisherViewSet, basename='publisher')
# router.register(r'reviews', views.ReviewViewSet, basename='review')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("home/", views.home, name="home"),
    # No longer needed as we'll use the main urls.py for API routing
]
