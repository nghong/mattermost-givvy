from django.shortcuts import render
from django.http import JsonResponse


response = {
    "message": "Hello"
}


def index(request):
    return JsonResponse(response)
