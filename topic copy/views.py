from django.shortcuts import render

# Create your views here.
def topic(request):
    return render(request,'topic.html')