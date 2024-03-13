from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'recipes/home.html', context={
        'name':'Bruno',
    })

def contato(request):
    return render(request,'templates/temp.html')

def sobre(request):
    return HttpResponse("Sobre")