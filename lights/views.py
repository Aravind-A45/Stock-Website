from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group, auth
from .models import *
from  django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import F

# Create your views here.

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user=auth.authenticate(username=username,password=password, email=email) 
            if user != None:
                auth.login(request,user)
                return redirect('home')
            else:
                return redirect('signup')
        except:
            return redirect('login')
 
    return render(request,'credentials/login.html')

def signup(request):
    details = User.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        con_password = request.POST.get('con_password')
        email = request.POST.get('email')

        if password == con_password:
          if User.objects.filter(username=username).exists():
              messages.info(request, f"Username already exists")
              return redirect('Register')

          user = User.objects.create_user(username=username, password=password, email=email)
          user = authenticate(username=username, password=password, email=email)
          if user is not None:
              return redirect('login')
          else:
              messages.error(request, "Invalid username or password.")
        else:
          messages.error(request, "Password and Confirm Password are not matching") 
    return render(request, 'credentials/signup.html')

def logout(request):
  auth.logout(request)
  return redirect('login')   

@login_required(login_url="login")
def home(request):
  stock = Stock.objects.all()
  return render(request, "credentials/home.html", {'stock':stock})

def add_to_cart(request, id):
    stock_name = Stock.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user, stock_name=stock_name
    )

    if created:
        cart_item.quantity+=1
        cart_item.save()
        messages.info(request, f"{stock_name.name} added to your watchlist.")
    else:
        messages.info(request, f"{stock_name.name} is already in your watchlist.")

    return redirect('home')

def excel(request):
  return render(request, "excel.html")
  
@login_required(login_url="login")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user, ordered=False)
    return render(request, 'cart/cart.html',{'cart_items':cart_items})

def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user, ordered=False)
    cart_item.delete()
    return redirect('cart')    

def submit(request, id):
        if request.method == "POST":
            for cart in Cart.objects.filter(user=request.user):
                item=Stock.objects.get(name=cart.stock_name)
                if (item.qty_aval - cart.quantity) < 0:
                    Cart.objects.filter(user=request.user).delete()
                    messages.warning(request, "Not Enough quantity available..")
                else:
                    Stock.objects.filter(name=cart.stock_name).update(qty_aval=F('qty_aval')-cart.quantity)
                    Mybuys.objects.create(product=cart.stock_name, quantity=cart.quantity, user=request.user)
                    Log.objects.create(product=cart.stock_name, quantity=cart.quantity, user=request.user)
                    Cart.objects.filter(user=request.user).delete()
        return redirect("home")    