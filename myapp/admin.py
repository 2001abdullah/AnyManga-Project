from django.contrib import admin
from .models import *
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps
# Register your models here.
app = apps.get_app_config('myapp')  # replace 'myapp' with your app's name

for model in app.get_models():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
