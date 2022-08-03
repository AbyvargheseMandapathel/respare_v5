

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('topic/<int:pk>/react/',views.react,name="react"), 
    #path('topic/<int:pk>/reactions/',views.reactions),
    path('topic/<int:pk>/reactstatus/',views.is_reacted) ,
    path('topic/<int:pk>/',views.topic,name='topic'),
    path('profile/',views.profile,name='profile'),


]
