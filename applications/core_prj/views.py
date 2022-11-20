import datetime

from django.http import HttpResponse, HttpRequest


def std_html_endpoint(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
