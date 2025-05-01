from django.forms import ModelForm
from .models import *


class User_form(ModelForm):
    class Meta:
        model=User
        fields='__all__'
        