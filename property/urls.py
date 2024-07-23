from django.urls import path
from .views import home, single_listing, properties_list
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name="homepage"),
    path('property/<int:property_id>/', single_listing, name='single_listing'),
    path('properties/', properties_list, name="properties")


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
