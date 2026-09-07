from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *

def Login(request):
    if request.user.is_authenticated:
        return redirect("home")
    context ={
        'error':''
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
        else:
            context['error']= '*Invailed Username or Password*'
            return render(request,'login.html',context)
    return render(request,'login.html',context)

def Logout(request):
    logout(request)
    return redirect('login')

def Signup(request):
    context ={
        "error":""
    }
    if request.method == "POST":
        user_check = User.objects.filter(username=request.POST['username'])
        if len(user_check)>0:
            context={
                "error" : "*User Name Is Already Exist"
            }
            return render(request,'signup.html',context)
        else:
            new_user= User(
                first_name = request.POST["first_name"],
                last_name = request.POST ["last_name"],
                username =request.POST["username"],
                email = request.POST["email"],
                age= request.POST["age"],
                dateofbirth=request.POST["dateofbirth"],
                role = request.POST["role"]
            )
            new_user.set_password(request.POST['password'])
            new_user.save()
            return redirect('login')
    return render(request,'signup.html',context)