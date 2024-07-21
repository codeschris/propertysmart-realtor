from django.shortcuts import render, redirect
from .forms import MultiplePhotoForm

# Create your views here.
def home(request):
    pass

"""def upload_photos(request):
    if request.method == 'POST':
        form = MultiplePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = MultiplePhotoForm()

    return render(request, 'upload_photos.html', {'form': form})"""
