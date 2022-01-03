from django.db import models

# Create your models here.

class App(models.Model):
    name = models.CharField(max_length=128)
    image = models.URLField(max_length=512)
    command = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name


class KeyValue(models.Model):
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    app = models.ForeignKey(App ,on_delete=models.CASCADE)

    def __str__(self):
        return self.key