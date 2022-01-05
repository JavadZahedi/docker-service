import docker
from docker.errors import ImageNotFound, APIError

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework import views, viewsets, status
from rest_framework.response import Response

from .models import App, Container
from .serializers import AppSerializer


docker_client = docker.from_env()


class AppViewSet(viewsets.ModelViewSet):

    queryset = App.objects.all()
    serializer_class = AppSerializer


class AppRunView(views.APIView):

    def get_object(self, id):
        return get_object_or_404(App.objects.all(), id=id)

    def get(self, id):
        app = self.get_object(id)
        env_vars = app.environment_variables
        labels = {
            'params': ', '.join(f'{key}={value}' for key, value in env_vars)
        }

        try:
            container = docker_client.containers.run(
                app.image, command=app.command or None, environment=env_vars,
                labels=labels, detach=True)
            Container.objects.create(container_id=container.id, app=app)

        except (ImageNotFound):
            return Response(
                data={'error': 'app\'s image not found'},
                status=status.HTTP_400_BAD_REQUEST)

        except (APIError):
            return Response(
                data={'error': 'an error occured when running the container'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppHistoryView(views.APIView):

    def get_object(self, id):
        return get_object_or_404(App.objects.all(), id=id)

    def get(self, id):
        app = self.get_object(id)
        data = {
            'runs': [container.attrs for container in app.containers.all()]
        }
        return Response(data=data, status=status.HTTP_200_OK) 
