from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm

def index(request) :
    form = SearchForm()
    return render(request , 'crawler_app/index.html' , {'form' : form})

def crawl(request) :
    if bool(request.POST) :
        print(request.POST)
        return HttpResponse("POST request acknowledged")
    else:
        return HttpResponse("No POST data recieved")
