from django.contrib import admin

from .models import App, EnvVar


admin.site.register(App)
admin.site.register(EnvVar)