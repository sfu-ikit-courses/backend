from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404

# Create your views here.


def page_not_found(request: HttpRequest, exception: Http404) -> HttpResponse:
    return render(request, "404.html", status=404)
