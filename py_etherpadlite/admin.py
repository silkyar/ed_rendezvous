# -*- coding: utf-8 -*-

from django.contrib import admin

from py_etherpadlite.models import *


class PadAuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class PadAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(PadServer)
admin.site.register(PadGroup)
admin.site.register(PadAuthor, PadAuthorAdmin)
admin.site.register(Pad, PadAdmin)
