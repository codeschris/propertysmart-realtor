from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Property, Profile, Feedback, ChatRoom
from .forms import LoginForm, UserRegistrationForm, PropertyForm, FeedbackForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    properties = Property.objects.all()
    return render(request, 'property/index.html', {'properties': properties})

def single_listing(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    feedbacks = Feedback.objects.filter(property=property).order_by('-created_at')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.property = property
            feedback.save()
            return redirect('single_listing', property_id=property_id)
    else:
        form = FeedbackForm()

    context = {
        'property': property,
        'feedbacks': feedbacks,
        'form': form
    }
    return render(request, 'property/property-single.html', context)

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

@login_required
def buyer_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'property/profile/buyer_profile.html', {'profile': profile})

@login_required
def realtor_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'property/profile/realtor_profile.html', {'profile': profile})

@login_required
def post_property_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.realtor = request.user
            property.save()
            return redirect('homepage')
    else:
        form = PropertyForm()
    return render(request, 'property/post_property.html', {'form': form})

def property_search(request):
    query = request.GET.get('q')
    if query:
        properties = Property.objects.filter(
            Q(location__icontains=query) | Q(title__icontains=query)
        )
    else:
        properties = Property.objects.all()
    return render(request, 'property/properties.html', {'properties': properties})

@login_required
def chatroom(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    chatroom, created = ChatRoom.objects.get_or_create(
        property=property,
        realtor=property.realtor,
        buyer=request.user
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = chatroom.realtor if request.user == chatroom.buyer else chatroom.buyer
            message.chatroom = chatroom
            message.save()
            return redirect('chatroom', property_id=property_id)
    else:
        form = MessageForm()

    messages = chatroom.messages.all().order_by('sent_at')

    context = {
        'property': property,
        'chatroom': chatroom,
        'messages': messages,
        'form': form
    }
    return render(request, 'property/chatroom.html', context)

def logout_view(request):
    logout(request)
    return redirect('logout_page')

def logout_page(request):
    return render(request, 'property/auth/logout.html')
