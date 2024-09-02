# https://dennis-sourcecode.herokuapp.com/24/
import random
# from Calender.extra_fun import gen_otp
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_list_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *

# For API Serialzers.
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions


class GetApiView(APIView):
    def get(self,request):
        todo_item=TodoModel.objects.all().values()
        return Response({"Message":"List of Todos", "Todo List":todo_item})

# class PostApiView(APIView):
#     def post(self,request):
#        serializer_data = TodoSerializer(data=request.data)
#        if serializer_data.is_valid():
#            serializer_data.save()
#            return Response({"Message":"New Todo Added!", "Todo":serializer_data.data})

class RegisterApiView(APIView):

   def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": user,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": LoginSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

{
"username" :"Kiran",
"first_name" :"Jasz Kaur",
"email" :"jass@gmail.com",
"password" :"todo"

}





def login(request):
    if request.method == "POST":
        # Get the value from input 
        phone = request.POST.get('number')
        password=request.POST.get('password')
        print(phone, password)
        user_auth = auth.authenticate(username=phone, password=password)
        print("USER_AUTH" , user_auth)
        
        if user_auth is not None:
            auth.login(request,user_auth)
            print(user_auth)
            messages.success(request, 'Auth User')
            return redirect('/show')
        else:
            messages.success(request, 'User not found')
            return redirect('/')

    return render(request,'login.html')    

def register(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try :
                user = User.objects.get(username=request.POST['uname'])
                return render(request,'register.html',{'error':"Username Has been Taken"}) 
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['number'],first_name=request.POST['uname'],email=request.POST['email'],password = request.POST['password1'])
                user.save()
                auth.login(request,user)               
                return redirect('/')
        else:
            return render(request,'register.html',{'error':"Password Dose Not Match"})
    else:
        return render(request,'register.html')

@login_required
def show(request):
    A_USER = request.user
    if request.method == "POST":
        todo= request.POST.get('todo')
        print(todo)
        if todo is not None:
            todo_item = TodoModel(todos = todo, user = request.user)
            todo_item.save()
            # print(todo_item)
    get_todo =TodoModel.objects.filter(user = request.user)
    return render(request,'show.html',{'get_item':get_todo,'A_USER':A_USER})

def logout(request):
    auth.logout(request)
    return redirect('/')

def delete(request,id):
    todo_delete = TodoModel.objects.get(id = id)
    print(todo_delete)
    todo_delete.delete()
    return redirect('/show')

def edit(request,id):
    if request.method =="POST":
        todo = request.POST.get('todo')
        # AUTH USER GET ID 
        todo_obj = TodoModel.objects.get(id=id)
        # For storing the value in particular field in
        # in Todo Model 'todos' field.
        todo_obj.todos = todo
        todo_obj.save()
        print("Todo",todo,"TODOS",todo_obj)
        return redirect('/show')
    else:
        # Return the particular value with id.
        todo = TodoModel.objects.filter(id=id)
        return render(request,'edit.html',{'todo':todo})

