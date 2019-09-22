from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.signals import user_logged_in

from problems.models import Concept
from py_etherpadlite.models import *

DEFAULT_USER_STATE = 'W'

class UserSession(models.Model):
    """Model to keep track of online users via their session info
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    # TODO: Need to change accounts app to have one session per user
    @staticmethod
    def user_logged_in_handler(sender, request, user, **kwargs):
        UserSession.objects.get_or_create(
            user = user,
            session_id = request.session.session_key
        )

    @staticmethod
    def delete_user_sessions(user):
        user_sessions = UserSession.objects.filter(user=user)
        for user_session in user_sessions:
            user_session.session.delete()

class UserPreference(models.Model):
    """Model to keep track of user preferences for skills and level
    """
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    LEVELS = (
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    )
    level = models.CharField(max_length=1, choices=LEVELS)

class UserState(models.Model):
    """Model to keep track of the live collaboration status
    """
    user_preference = models.ForeignKey(UserPreference, on_delete=models.CASCADE)

    STATE = (
        ('W', 'Waiting'),
        ('C', 'Collaborating'),
    )
    state = models.CharField(max_length=1, choices=STATE, default=DEFAULT_USER_STATE)
    # We needn't delete user state if the pad they are working on gets deteted
    pad = models.ForeignKey(Pad, models.SET_NULL, default=None, null=True, blank=True)

# Register signal handles
user_logged_in.connect(UserSession.user_logged_in_handler)
user_logged_in.disconnect(UserSession.delete_user_sessions)
