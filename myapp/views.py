from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import User_form,ShippingForm
from django.contrib.auth.decorators import login_required
import uuid
from decimal import Decimal

# Create your views here.
def home(request):
    manga_preview=Manga.objects.all()[:8]
    merch_preview=Merch.objects.all()
    naruto=Manga.objects.get(name='Naruto:Shippuden')
    context={
        'manga_preview':manga_preview,
        'merch_preview':merch_preview,
        'naruto':naruto
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
    if request.user.is_authenticated:
        return redirect('home')

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Manga, Merch

@login_required
def add_to_cart(request, product_type, product_id):
    user = request.user

    if product_type == 'manga':
        product = get_object_or_404(Manga, id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=user, manga_p=product, merch_p=None
        )
    elif product_type == 'merch':
        product = get_object_or_404(Merch, id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=user, merch_p=product, manga_p=None
        )
    else:
        messages.error(request, "Invalid product type.")
        return redirect('home')

    if not created:
        cart_item.save()

    # Show success message
    messages.success(request, "✅ Added to cart!")

    return redirect('home')

@login_required
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    display_items = []
    for item in cart_items:
        if item.manga_p:
            product = item.manga_p
            product_type = 'manga'
            product_id = item.manga_p.id
        else:
            product = item.merch_p
            product_type = 'merch'
            product_id = item.merch_p.id

        display_items.append({
            'name': product.name,
            'price': product.price,
            'picture_url': product.picture.url,
            'category': product.category,
            'type': 'manga' if item.manga_p else 'merch',
            'id': product.id,
        })

    context = {
        'display_items': display_items
    }
    return render(request, 'myapp/view_cart.html', context)

@login_required
def remove_from_cart(request, product_type, product_id):
    user = request.user

    if product_type == 'manga':
        product = get_object_or_404(Manga, id=product_id)
        cart_item = Cart.objects.filter(user=user, manga_p=product).first()
    elif product_type == 'merch':
        product = get_object_or_404(Merch, id=product_id)
        cart_item = Cart.objects.filter(user=user, merch_p=product).first()
    else:
        messages.error(request, "Invalid product type.")
        return redirect('view_cart')

    if cart_item:
        cart_item.delete()
        messages.success(request, "🗑️ Item removed from cart.")
    else:
        messages.warning(request, "Item not found in your cart.")

    return redirect('view_cart')


@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('home')  # Replace with your cart view name

    # Calculate total
    total_price = 0
    for item in cart_items:
        if item.manga_p:
            total_price += item.manga_p.price or 0
        elif item.merch_p:
            total_price += item.merch_p.price or 0

    if request.method == 'POST':
        # Map HTML input names to model field names
        data = {
            'full_name': request.POST.get('firstname'),
            'email': request.POST.get('email'),
            'phone': '0000000000',  # Hardcoded unless added in your form
            'address': request.POST.get('address'),
            'country': request.POST.get('country'),  # assuming state == country
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
        }
        form = ShippingForm(data)

        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = user
            shipping.save()

            # Create Payment
            payment = Payment.objects.create(
                user=user,
                amount=Decimal(total_price),
                payment_method='Credit Card',  # Placeholder
                status='Pending',
                transaction_id=str(uuid.uuid4())
            )

            # Create Order
            order = Order.objects.create(
                user=user,
                payment=payment,
                total_amount=Decimal(total_price),
                shipping_address=shipping.address,
                status='Pending'
            )

            # Clear cart (optional)
            cart_items.delete()

            messages.success(request, "Order placed successfully!")
            return redirect('home')  # Replace with your success page
        else:
            messages.error(request, "Please correct the form errors.")

    else:
        form = ShippingForm()

    return render(request, 'myapp/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total_price
    })
def manga_view(request,manga_id):
    manga=get_object_or_404(Manga,id=manga_id)
    context={
        'manga':manga
    }
    return render(request,'myapp/manga-view.html',context=context)
def merch_view(request,merch_id):
    merch=get_object_or_404(Merch,id=merch_id)
    context={
        'merch':merch
    }
    return render(request,'myapp/merch_view.html',context=context)