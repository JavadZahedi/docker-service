from django.contrib import admin

from .models import App, Container, EnvVar


admin.site.register(App)
admin.site.register(EnvVar)
admin.site.register(Container)