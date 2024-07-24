from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Property, Profile
from .forms import LoginForm, UserRegistrationForm

def home(request):
    properties = Property.objects.all()
    return render(request, 'property/index.html', {'properties': properties})

def single_listing(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    return render(request, 'property/property-single.html', {'property': property})

def properties_list(request):
    properties = Property.objects.all()
    return render(request, 'property/properties.html', {'properties': properties})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                bio=form.cleaned_data.get('bio'),
                address=form.cleaned_data.get('address'),
                preferences=form.cleaned_data.get('preferences')
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'property/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email_address = form.cleaned_data.get('email_address')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email_address=email_address, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid email address or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()
    
    return render(request, 'property/auth/login.html', {'form': form})
