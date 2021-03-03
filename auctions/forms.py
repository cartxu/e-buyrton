from django import forms
from django.forms import ModelForm
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startbid', 'category', 'image']
        widgets = {
          'bid': forms.TextInput(attrs={'class': 'form-control'})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]
        labels = {"bid": ""}
        widgets = {
          'bid': forms.TextInput(attrs={'class': 'form-control'})
        }

class CommentsForm(ModelForm):
    class Meta:
      model = Comments
      fields = ['comment']
      
