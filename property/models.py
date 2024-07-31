from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email_address, name, phone_number, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email field must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, name=name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email_address, name, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    BUYER = 'Buyer'
    REALTOR = 'Realtor'
    USER_TYPE_CHOICES = [
        (BUYER, 'Buyer'),
        (REALTOR, 'Realtor'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    email_address = models.EmailField(max_length=255, unique=True, null=False)
    phone_number = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=100, null=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=False)
    created_at = models.DateField(auto_now_add=True, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['name', 'phone_number', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    bio = models.TextField(null=False)
    address = models.CharField(max_length=255, null=False)
    preferences = models.TextField(null=False)
    updated_at = models.DateField(auto_now=True, null=False)
    
    def __str__(self):
        return self.user.name


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    created_at = models.DateField(auto_now_add=True, null=False)
    
    def __str__(self):
        return f'Feedback by {self.user.name}'

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, null=False)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    sent_at = models.DateField(auto_now_add=True, null=False)
    
    def __str__(self):
        return f'Message from {self.sender.name} to {self.receiver.name}'

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    realtor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Realtor'}, null=False)
    title = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    location = models.CharField(max_length=255, null=False)
    property_type = models.CharField(max_length=100, null=False)
    bedrooms = models.IntegerField(null=False)
    bathrooms = models.IntegerField(null=False)
    area = models.FloatField(null=False)
    listed_at = models.DateField(auto_now_add=True, null=False)
    primary_photo = models.ImageField(upload_to='property_photos/', null=True, blank=True)

    def __str__(self):
        return self.title


#class Photo(models.Model):
#    photo_id = models.AutoField(primary_key=True)
#    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE, null=False)
#    image = models.ImageField(upload_to='property_photos/', null=False)
#    created_at = models.DateField(auto_now_add=True, null=False)
#
#    def __str__(self):
#        return f'Photo of {self.property.title}'


class SearchFilter(models.Model):
    filter_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    location = models.CharField(max_length=150, null=False)
    price_min = models.FloatField(null=False)
    price_max = models.FloatField(null=False)
    property_type = models.CharField(max_length=50, null=False)
    bedrooms = models.IntegerField(null=False)
    bathrooms = models.IntegerField(null=False)
    area_min = models.FloatField(null=False)
    area_max = models.FloatField(null=False)
    created_at = models.DateField(auto_now_add=True, null=False)
    
    def __str__(self):
        return f'Search Filter by {self.user.name}'
