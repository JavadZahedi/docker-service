import docker

from django.db import models

docker_client = docker.from_env()

class App(models.Model):
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=512)
    command = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

    @property
    def environment_variables(self):
        vars_dict = {}
        for env_var in self.env_vars:
            vars_dict[env_var.key] = env_var.value
        return vars_dict


class KeyValue(models.Model):
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    app = models.ForeignKey(
        App ,on_delete=models.CASCADE, related_name='env_vars')

    def __str__(self):
        return self.key


class Container(models.Model):
    container_id = models.CharField(max_length=64)
    app = models.ForeignKey(
        App ,null=True, on_delete=models.SET_NULL, related_name='containers')

    def __str__(self):
        return self.container_id

    @property
    def attrs(self):
        container = docker_client.containers.get(self.container_id)
        return {
            'exec_time': container.attrs['Created'],
            'params': container.labels['params'],
            'status': container.status,
        }
