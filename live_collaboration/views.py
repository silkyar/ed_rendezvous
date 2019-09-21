from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, learner! Collaboration will commence momentarily!")

def matching(request):
    return render(request, 'live_collaboration/matching.html', {})
