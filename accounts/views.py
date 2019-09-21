from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from py_etherpadlite.models import Pad

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        content_type = ContentType.objects.get_for_model(Pad)
        permission_pad_view = Permission.objects.get(codename='view_pad', content_type=content_type)
        # TODO: Might not need change_pad permission
        permission_pad_edit = Permission.objects.get(codename='change_pad', content_type=content_type)

        self.object = form.save()
        user = get_user_model().objects.get(username=form.cleaned_data['username'])
        user.user_permissions.set([permission_pad_view, permission_pad_edit])
        return HttpResponseRedirect(self.get_success_url())
