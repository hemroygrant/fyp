from django import forms

from .models import Image

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control bg-secondary'}),
			}