from django.shortcuts import render
from tables.models import Review

# Create your views here.


def index(request):
    reviews = Review.objects.all().order_by('-id')[:3]
    return render(request, 'home/index.html', {'reviews': reviews})
