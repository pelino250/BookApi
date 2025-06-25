"""
URL configuration for BookApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views as token_views
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from books import views as books_views

# Create API routers
v1_router = routers.DefaultRouter()
v1_router.register(r"books", books_views.BookViewSet, basename="book")
# The following viewsets will be added back later
# v1_router.register(r'authors', books_views.AuthorViewSet, basename='author')
# v1_router.register(r'publishers', books_views.PublisherViewSet, basename='publisher')
# v1_router.register(r'reviews', books_views.ReviewViewSet, basename='review')

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version="v1",
        description="A RESTful API for managing books, authors, publishers, and reviews",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Frontend views
    path("", include("books.urls")),
    # API authentication
    path("api/auth/", include("rest_framework.urls")),
    path("api/token/", token_views.obtain_auth_token, name="api-token"),
    # API versioning
    path("api/v1/", include(v1_router.urls)),
    # Swagger documentation URLs
    re_path(
        r"^api/docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
