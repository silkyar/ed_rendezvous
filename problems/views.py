from django.db import IntegrityError, OperationalError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from problems.models import *
from live_collaboration.models import *

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
    skills = Skill.objects.filter(
            Q(topics__name__icontains = topic_name))

    context = {
        'skills': skills
    }
    return render(request, 'preferences/preferences.html', context)

def process_preferences(request):
    concept_preference_key = request.POST.get('concept_radiobtn')

    # Get the sessions associated with this user
    if request.user.is_authenticated:
        user = request.user
        user_sessions = UserSession.objects.filter(user=user)

        print("I am in process preferences")
        # Insert/update user preferences with the current preferences
        # TODO: Change form to take in level preference too
        for user_session in user_sessions:
            concept = Concept.objects.get(
                    pk=concept_preference_key)
            try:
                obj, created = \
                    UserPreference.objects.update_or_create(
                        user_session=user_session,
                        defaults={'concept': concept
                                 ,'level':'B'
                                 },
                    )

                # Insert/update user state. The default state is waiting
                UserState.objects.update_or_create(
                    user_preference = obj,
                    defaults={'state':DEFAULT_USER_STATE},
                )
                return HttpResponseRedirect('/live_collaboration/matching')
            # TODO: Need to figure out why we get 2 requests
            except OperationalError as e:
                return HttpResponseRedirect('/live_collaboration/matching')

    return HttpResponseRedirect('accounts/login')
