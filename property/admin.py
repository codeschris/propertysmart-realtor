from django.contrib import admin
from .models import User, Profile, Property, Feedback, Message, Photo, SearchFilter

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_address', 'phone_number', 'user_type', 'created_at')
    search_fields = ('name', 'email_address', 'phone_number')
    list_filter = ('user_type', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'updated_at')
    search_fields = ('user__name', 'address')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'realtor', 'price', 'location', 'listed_at')
    search_fields = ('title', 'realtor__name', 'location')
    list_filter = ('property_type', 'bedrooms', 'bathrooms', 'listed_at')

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

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('property', 'created_at')
    search_fields = ('property__title',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(SearchFilter, SearchFilterAdmin)
