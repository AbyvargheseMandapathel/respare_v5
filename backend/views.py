from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from.models import UserProfile
import re
from urllib.request import Request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from backend import models
from backend.models import Reaction, Topic, Choice
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ChoiceSerializer,ChoiceIdSerializer
from django.core.files.storage import FileSystemStorage
# Create your views here.
def home(request):
    recommended=Topic.objects.all()[:20]
    trending=Topic.objects.all()[20:]
    slide=trending[:5]
    return render(request,'index.html',{'name':'Aravind','recommended':list(recommended),'trending':list(trending),'slide':slide})

def register(request):

    if request.method == "POST":
      
      fname = request.POST['fname']
      lname = request.POST['lname']
      uname = request.POST['uname']
      email = request.POST['email']
      pass1 = request.POST['pass1']
      pass2 = request.POST['pass2']
      

      myuser = User.objects.create_user(uname, email, pass1)
      myuser.first_name=fname
      myuser.last_name=lname

      myuser.save()

      messages.success(request, "Your account has been successfully created")

      return redirect('signin')

    
    return render(request,"register.html")


def signin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=uname, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,'index.html',{"fname":fname})

        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def topic(request,pk):
    topic=Topic.objects.get(id=pk)
    reactions=Choice.objects.filter(topic_id=pk)
    return render(request,'topic2.html',{'topic':topic,'reactions':list(reactions),'message':None,'percent':None})

@api_view(['GET','POST'])
def react(request,pk):
    #print(request.user.id,request.user.is_authenticated,request.data)
    if not request.user.is_authenticated: 
          return Response("0")
    else:
        user=request.user
        deserializer=ChoiceIdSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        choice_id=deserializer.validated_data['id']
        if Reaction.objects.filter(user_id=user).filter(topic_id=pk).exists():
            reaction=Reaction.objects.filter(user_id=user).get(topic_id=pk)
            old_choice=Choice.objects.get(id=reaction.choice_id)
            if old_choice.count >0:
                old_choice.count-=1
            else:
                old_choice.count=0
            old_choice.save()
            new_choice=Choice.objects.get(id=choice_id)
            new_choice.count+=1
            new_choice.save()
            reaction.choice_id=choice_id
            reaction.time=datetime.now()
            reaction.save()
        else:
            reaction=Reaction(time=datetime.now(),choice_id=choice_id,user_id=user.id,topic_id=pk)
            reaction.save()
        return Response("Okk")

@api_view(['GET','POST'])
def is_reacted(request,pk):
    if not request.user.is_authenticated:
        return Response("0")
    elif Reaction.objects.filter(user_id=request.user).filter(topic_id=pk).exists():
        choicelist=Choice.objects.filter(topic_id=pk)  
        serializer=ChoiceSerializer(choicelist,many=True)
        return Response(serializer.data)
    return Response("0")

#@api_view(['GET'])
#def reactions(request,pk):
@login_required(login_url='/signin')
def profile(request):
    context = {
        "user": request.user
    }
    return render(request,"user.html", context)

#@login_required
#def profile (request,user_id):
#    if request.method == 'POST':
#        user_obj = User.objects.get(id=user_id)
#        user_profile_obj = UserProfile.objects.get(id=user_id)
#        user_img = request.FILES['user_img']
#        fs_handle = FileSystemStorage()
#        img_name = 'images/user_{0}'.format(user_id)
#        if fs_handle.exists(img_name):
#            fs_handle.delete(img_name)
#        fs_handle.save(img,user_img)
#        user_profile_obj.profile_img=img_name
#        user_profile_obj.save()
#        user_profile_obj.refresh_from_db()
#        return render(request,'user.html',{'my_profile':user_profile_obj})
#        if (request.user.is_authenticated and request.user.id == user_id):
#            user_obj=User.objects.get(id=user_id)
#            user_profile = UserProfile.objects.get(id=user_id)
#            return render(request,'user.html',{'my_profile':user_profile})
