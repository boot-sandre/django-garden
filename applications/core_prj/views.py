# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime


def endpoint(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
