from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Example URL pattern
    # Add your URL patterns here
]
