from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse

def index(request):
    return HttpResponseRedirect(reverse('APP_Blog:blog_list'))