from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'reviews', views.ReviewViewSet, basename='review')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
]
