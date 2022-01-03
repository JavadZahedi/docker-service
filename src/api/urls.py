from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'apps', views.AppViewSet)

urlpatterns = [
    # POST GET DELETE PUT PATCH
    path('', include(router.urls)),
    # GET
    path('run/<int:id>', views.AppRunView),
    # GET
    path('history/<int:id>', views.AppHistoryView),
]
