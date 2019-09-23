from django.shortcuts import render
from django.http import HttpResponse
from live_collaboration.models import *
import json


def index(request):
    return HttpResponse("Hello, learner! Collaboration will commence momentarily!")

def matching(request):
    return render(request, 'live_collaboration/matching.html', {})

def matching_poll(request):
    data = {'status': 0, 'url':'/py_etherpadlite/etherpad/8'}
    user = request.user
    # Let's see if we have created a pad for this user and put them in collaboration state
    # TODO: Pick up first session. Make sure we only create one session in future
    user_session = UserSession.objects.filter(user=user)[0]
    user_preference = UserPreference.objects.get(user_session=user_session)
    user_state = UserState.objects.get(user_preference=user_preference)
    
    if user_state.state == 'C' and user_state.pad:
        data = { 'status': 1
               , 'url':'/py_etherpadlite/etherpad/{}'.format(user_state.pad.pk)
               }
    return HttpResponse(json.dumps(data), content_type='application/json')
