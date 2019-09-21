from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from live_collaboration.models import *
from py_etherpadlite.models import *

import random

def get_group_name(user_a, user_b):
    return user_a.username + '_' + user_b.username

def get_pad_name():
   """Return random name for the pad
   """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(8))

def create_or_get_pad_group(user_a, user_b):
    # One group per unique pair of peers

    # Django auth group
    group_name = get_group_name(user_a, user_b)
    Group.objects.get_or_create(name=group_name)
    group = Group.objects.get(name=group_name)

    # Add the groups to both the users
    user_a.groups.add(group)
    user_b.groups.add(group)

    # PadGroup and PadAuthor models have custom object creation
    # logic, and so we will use save() for creation
    server = PadServer.objects.all()[0]

    # PadGroup creation
    if not PadGroup.objects.filter(group=group).exists():
        pad_group = PadGroup(group=group, server=server)
        pad_group.save()

    # PadAuthors creation
    if not PadAuthor.objects.filter(user=user_a).exists():
        author_a = PadAuthor(user=user_a, server=server)
        author_a.save()

    if not PadAuthor.objects.filter(user=user_b).exists():
        author_b = PadAuthor(user=user_b, server=server)
        author_b.save()

    # Adding PadAuthors to PadGroup is done automatically during
    # PadAuthor creation as long as the user corresponding to
    # PadAuthor is in group corresponding to PadGroup
    return pad_group

def random_match(user_preference):
    """This is a simple matching algorithm that returns a
    random peer who has same preferences
    """
    user = user_preference.user_session.user
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
            return peer_preferences[peer_index]

    return None

@receiver(post_save, sender=UserPreference)
def user_preferences_updated(sender, instance, *args, **kwargs):
    """This method is executed whenever we get a signal
    that user preferences table had pre_save event which
    signifies an insertion or an update.
    This is a good time to run peer matching.
    """
    user_preference = instance
    peer_preference = random_match(user_preference)

    if peer_preference:
        peer = peer_preference.user_session.user
        user = user_preference.user_session.user
        print("You have been matched with {}".format(peer.username))

        # Create a new peer group for the user and the peer
        pad_group = create_or_get_pad_group(user, peer)

        # Create a new pad for the user and the peer
        pad = Pad(name=get_pad_name(), server=pad_group.server, group=pad_group)
        pad.save()

        # Mark user and peer in collaborating state
        UserState.objects.filter(user_preference=user_preference).update(state='C')
        UserState.objects.filter(user_preference=peer_preference).update(state='C')

    # We don't need to wait here if there are no peers to match with.
    # When another user triggers this signal, this user might get that user as a peer
