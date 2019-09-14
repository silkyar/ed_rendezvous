from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from problems.models import *

def index(request):
    return HttpResponse("Hello, leaner. You're at the problems index.")


def topics(request):
    topics = Topic.objects.all()
    context = {
        'topics': topics
    }
    return render(request, 'home.html', context)

def preferences(request, topic_name):
    # Get all the skills for this topic
    topic = Topic.objects.get(pk=topic_name)
    skills = Skill.objects.filter(Q(topics__name__icontains = topic_name))

    context = {
        'skills': skills
    }
    return render(request, 'preferences/preferences.html', context)
