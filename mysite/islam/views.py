from django.shortcuts import render
from django.http import HttpResponse
from .prayers import get_prayers


def index(request):

    return HttpResponse(get_prayers())