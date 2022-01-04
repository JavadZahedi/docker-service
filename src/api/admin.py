from django.contrib import admin

from .models import App, KeyValue


admin.site.register(App)
admin.site.register(KeyValue)