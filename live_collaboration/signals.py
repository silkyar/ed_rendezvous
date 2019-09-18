from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from live_collaboration.models import *

import random

@receiver(post_save, sender=UserPreference)
def user_preferences_updated(sender, instance, *args, **kwargs):
    """This method is executed whenever we get a signal
    that user preferences table had pre_save event which
    signifies an insertion or an update.
    This is a good time to run peer matching.
    """
    peer = random_match(instance.user_session.user)

    print("You have been matched with {}".format(peer.username))

    # Create a new pad group for the user and the peer

    # Create a new pad for the user and the peer

    # Mark user and peer in collaborating state


# Helper Methods

def random_match(user):
    """This is a simple matching algorithm that returns a
    random peer who has same preferences
    """

    user_sessions = UserSession.objects.filter(user=user)

    # TODO: This won't be needed when we have just one user per session
    if user_sessions:
        user_session = user_sessions[0]
        user_preference = UserPreference.objects.get(user_session=user_session)

        concept = user_preference.concept
        peer_preferences = UserPreference.objects.filter(
            concept=concept
            ).exclude(
            Q(user_session=user_session)
            ).filter(
            userstate__state = 'W'
            )

        if peer_preferences:
            # Randomize
            peer_index = random.randint(0, peer_preferences.count() - 1)
            return peer_preferences[peer_index].user_session.user

    return None
