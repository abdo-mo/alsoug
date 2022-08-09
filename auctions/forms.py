from turtle import title
from django.forms import ModelForm
from auctions.models import *
from django import forms

class UploadImage(ModelForm):
    title = forms.CharField()
    description = forms.Textarea()
    image_upload = forms.ImageField()
    
    class Meta():
        model = Listing
        fields = ['image_upload']


