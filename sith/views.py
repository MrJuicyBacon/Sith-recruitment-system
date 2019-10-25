from django.shortcuts import render, redirect, HttpResponse


def index(request):
    return render(request, 'sith/index.html')

