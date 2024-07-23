from django.contrib import admin
from .models import User, Profile, Property, Feedback, Message, SearchFilter
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_address', 'phone_number', 'user_type', 'created_at')
    search_fields = ('name', 'email_address', 'phone_number')
    list_filter = ('user_type', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'updated_at')
    search_fields = ('user__name', 'address')

from django.utils.html import format_html

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'realtor', 'price', 'location', 'listed_at', 'display_photo')
    search_fields = ('title', 'realtor__name', 'location')
    list_filter = ('property_type', 'bedrooms', 'bathrooms', 'listed_at')

    def display_photo(self, obj):
        if obj.primary_photo:
            return format_html('<img src="{}" width="100" />', obj.primary_photo.url)
        return 'No Image'
    display_photo.short_description = 'Primary Photo'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__name', 'content')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'sent_at')
    search_fields = ('sender__name', 'receiver__name', 'content')

class SearchFilterAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'price_min', 'price_max', 'created_at')
    search_fields = ('user__name', 'location')
    list_filter = ('property_type', 'bedrooms', 'bathrooms')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(SearchFilter, SearchFilterAdmin)
