from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class User_form(ModelForm):
    class Meta:
        model=User
        fields='__all__'

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['full_name', 'email', 'phone', 'address', 'country', 'city', 'zip_code']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
class register_form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

