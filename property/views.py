from django.shortcuts import render, get_object_or_404
from .models import Property

def home(request):
    properties = Property.objects.all()
    return render(request, 'property/index.html', {'properties': properties})

def single_listing(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    return render(request, 'property/property-single.html', {'property': property})

def properties_list(request):
    properties = Property.objects.all()
    return render(request, 'property/properties.html', {'properties': properties})
