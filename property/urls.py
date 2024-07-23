from django.urls import path
from .views import home, single_listing
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name="homepage"),
    path('property/<int:property_id>/', single_listing, name='single_listing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
