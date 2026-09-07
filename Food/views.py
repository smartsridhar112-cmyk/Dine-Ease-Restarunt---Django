from django.shortcuts import render,redirect,get_object_or_404
from .models import *
import razorpay
from django.db.models import Q
from django.utils import timezone

RAZORPAY_KEY_ID  = "rzp_test_TPJdZ0ry8P3NMO"

RAZORPAY_KEY_SECRET  = "N1ErlgbyTdGv0HmGvlQ7ajEj"

def HomePage(request):
    category = Category.objects.all()
    context = {
        'category':category,
        'current_category': ''  
    }
    return render(request,'home.html',context)

def FoodCategory(request,category_name=None,food_name=None):
    foods= Category.objects.all()
    if category_name in ["veg","non-veg"]:
        foods= foods.filter(categories=category_name)
    if food_name :
        foods= foods.filter(food_category=food_name)
    return render(request,'category.html',{'category':foods,'current_category':category_name})

def AddCart(request, id):
    food = get_object_or_404(Category, id=id)
    cart_item, created = Cart.objects.get_or_create(
        category=food,
        food_name= food.food_name,
        defaults={'quantity': 1, 'amount': food.food_price}
    )
    if not created:
        cart_item.quantity
        cart_item.amount = cart_item.category.food_price * cart_item.quantity
        cart_item.save()
    return redirect('categories_list')

def UpdateQuantity(request,id,action):
    cart = get_object_or_404(Cart, id=id)
    if action == "increase":
        cart.quantity +=1
    elif action == "decrease" and cart.quantity>1:
        cart.quantity -=1
    cart.amount = cart.category.food_price * cart.quantity
    cart.save()
    return redirect('all_cart')

def AllCart(request):
    cart = Cart.objects.all()
    return render(request,'cart.html',{'cart':cart})

def RemoveCart(request,id):
    removecart = Cart.objects.get(id=id)
    removecart.delete()
    return redirect('all_cart')

def AddOrder(request,id):
    cart =get_object_or_404(Cart,id=id)
    order,created= Order.objects.get_or_create(
        user = request.user,
        category = cart.category,
        status="pending",
        defaults={
            'quantity': cart.quantity,
            'amount': cart.amount
        }
    )
    if not created:
        order.quantity += cart.quantity
        order.amount = cart.category.food_price * order.quantity
        order.save()
    cart.delete()
    return redirect('all_order',)


def AllOrder(request):
    orders = Order.objects.filter(user=request.user,status="pending")
    order_total = sum(order.amount for order in orders)
    return render(request,'order.html',{'orders':orders, 'order_total': order_total})

def RemoveOrder(request,id):
    removeorder = Order.objects.get(id=id)
    removeorder.delete()
    return redirect('all_order')

def CheckOut(request):
    orders = Order.objects.filter(user=request.user, status="pending")
    total = sum(order.amount for order in orders)

    if total <1 :
        return render(request,"checkout.html",{
            'orders': orders,
            "total": total,
            "error": "Order amount atleast 1.Rs"
        })

    client= razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET ))

    razorpay_order = client.order.create({
        "amount" : int(total * 100),
        "currency": "INR",
        "payment_capture" : 1
    })

    context = {
    "orders": orders,
    "total": total,
    "razorpay_order": razorpay_order,
    "razorpay_key": RAZORPAY_KEY_ID 
    }

    return render(request,'checkout.html',context)

def payment_success(request):
    orders = Order.objects.filter(user= request.user)

    for order in orders:
        order.status="paid"
        order.payment_id="TEST_PAYMENT"
        order.save()

        MyOrders.objects.get_or_create(
            category = order.category,
            food_name= order.category.food_name,
            order=order,
            amount= order.amount
        )
    return render(request, 'sucess.html') 
    

def MyOrder(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'myorders.html',{'allorders':orders})


def Search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Category.objects.filter(
            Q(food_name__icontains = query) |
            Q(food_category__icontains = query) |
            Q(categories__icontains = query)
        )
    return render(request,'search.html',{'results':results,'query':query})