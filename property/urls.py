from django.urls import path
from .views import (home, single_listing, properties_list, 
                    login_view, register, buyer_profile_view, 
                    realtor_profile_view, post_property_view, logout_page, 
                    logout_view)
from django.conf.urls.static import static
from django.conf import settings
from pwa import views as pwa_views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', home, name="homepage"),
    path('property/<int:property_id>/', single_listing, name='single_listing'),
    path('properties/', properties_list, name="properties"),
    path('auth/login/', login_view, name="login"),
    path('auth/register/', register, name='register'),
    path('profile/buyer/', buyer_profile_view, name='buyer_profile'),
    path('profile/realtor', realtor_profile_view, name='realtor_profile'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/logout_page/', logout_page, name='logout_page'),
    path('post_property/', post_property_view, name='post_property'),
    path('offline/', cache_page(60 * 15)(pwa_views.offline), name='offline'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
