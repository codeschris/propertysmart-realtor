from django import forms
from .models import Property, Photo

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Handle multiple file uploads
        if isinstance(data, list):
            result = [super().clean(file) for file in data if file]
        else:
            result = super().clean(data)
        return result

class MultiplePhotoForm(forms.Form):
    property = forms.ModelChoiceField(queryset=Property.objects.all())
    images = MultipleFileField(label='Select photos', required=False)

    def save(self, commit=True):
        property = self.cleaned_data['property']
        images = self.files.getlist('images')  # Handle multiple files

        photo_instances = []
        for image in images:
            photo_instance = Photo(property=property, image=image)
            if commit:
                photo_instance.save()
            photo_instances.append(photo_instance)

        return photo_instances
