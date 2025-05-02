from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import User_form

# Create your views here.
def home(request):
    manga_preview=Manga.objects.all()
    merch_preview=Merch.objects.all()
    context={
        'manga_preview':manga_preview,
        'merch_preview':merch_preview
    }
    return render(request, template_name='myapp/home.html',context=context)

def manga(request):
    manga_preview = Manga.objects.all()
    context = {
        'manga_preview': manga_preview,
    }
    return render(request,template_name='myapp/manga.html',context=context)

def merch(request):
    merch_preview = Merch.objects.all()
    context = {
        'merch_preview': merch_preview
    }
    return render(request, template_name='myapp/merch.html', context=context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'myapp/login_view.html')


def Register(request):
      if request.method=='POST':
          form=User_form(request.POST)
          if form.is_valid():
              form.save()
              messages.success(request,"account opened successfully")
              return redirect('home')
          else:
              messages.error(request,"invalid")
      else:
          form=User_form()
      context={
          'form':form
      }
      return render(request,template_name='myapp/register.html',context=context)

            