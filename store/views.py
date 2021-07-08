from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse 

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # Not used yet, it is used when the login fom is required

from .models import *
import json
import datetime

from .utils import cookieCart  # imported utils.py, cookieCart in order to "DRY(Don't Repeat Yourself)"
from .utils import cartData # imported utils.py, cartData in order to "DRY(Don't Repeat Yourself)"
from .utils import guestOrder # imported utils.py, cartData in order to "DRY(Don't Repeat Yourself)"

from .forms import  CreateUserForm 
from .decorators import unauthenticated_user #allowed_users

# @allowed_users(allowed_roles = ["admin"])
def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context = {"products" : products, "cartItems":cartItems}

    return render(request, 'store/store.html', context) 

def cart(request): 
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"] 


    context = {"items":items, "order":order, "cartItems":cartItems} 
    return render(request, 'store/cart.html', context) 

def checkout(request): 
    data = cartData(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]

    context = {"items":items, "order":order, "cartItems":cartItems} 
    return render(request, 'store/checkout.html', context ) 
 
def updateItem(request): 
    data = json.loads(request.body) 
    productId = data['productId'] 
    action = data['action'] 

    print("Action:", action) 
    print("ProductId:", productId) 

    customer = request.user.customer 
    product = Product.objects.get(id=productId) 
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 
    if action =='add': 
        orderItem.quantity += 1 

    elif action=="remove": 
        orderItem.quantity -= 1 
    
    orderItem.save() 
 
    if orderItem.quantity <= 0: 
        orderItem.delete() 

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else: 
        print("User is not logged in...")
        print("COOKIES: ", request.COOKIES)
        
        customer, order = guestOrder(request, data)

    # Conforming the total regardless who is checking out
    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    # If the shipping for the item is true, regardless
    # who is checking out, the shipping column appears
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address= data["shipping"]["address"],
            city= data["shipping"]["city"],
            country= data["shipping"]["country"],
            region_district = data["shipping"]["region_district"],
            zipcode= data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment complete!", safe=False)


def detail(request, product_id):
    data = cartData(request)
    cartItems = data["cartItems"]

    product = Product.objects.get(pk=product_id)
    context = {"cartItems":cartItems, "product": product} 
    return render(request, 'store/detail.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            # created = Customer.objects.create(username=username, name=username, email=email)
            
            messages.success(request, 'Account was successfully created for ' + username)
            return redirect('user_login')

    context = {'form':form }
    return render(request, 'store/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store_store')
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, 'store/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect("store_store")


    









