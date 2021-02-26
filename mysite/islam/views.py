from django.shortcuts import render
from django.http import HttpResponse
from .prayers import get_prayers


def index(request):
    names = []
    times = []
    for name, time in get_prayers():
        times.append(time)
        names.append(name)
    return render(request, 'prayers.html', context={'prayers': get_prayers()})