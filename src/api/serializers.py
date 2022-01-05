from rest_framework import serializers

from .models import App, EnvVar


class EnvVarSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = EnvVar
        fields = ['key', 'value']


class AppSerializer(serializers.ModelSerializer):

    env_vars = EnvVarSerializer(many=True)

    def create_new_env_vars(self, new_env_vars, app):
        added_keys = set() # Store added keys to prevent duplicate keys
        for new_env_var in new_env_vars:
            key = new_env_var['key']
            value = new_env_var['value']
            if key not in added_keys:
                added_keys.add(key)
                EnvVar.objects.create(key=key, value=value, app=app)

    def create(self, validated_data):
        new_env_vars = validated_data.pop('env_vars')
        new_app = super().create(validated_data)
        self.create_new_env_vars(new_env_vars, new_app)
        return new_app

    def update(self, instance, validated_data):
        new_env_vars = validated_data.pop('env_vars')
        instance = super().update(instance, validated_data)
        old_env_vars = instance.env_vars.all()
        old_env_vars.delete()
        self.create_new_env_vars(new_env_vars, instance)
        return instance

    class Meta:
        model = App
        fields = ['id', 'name', 'image', 'command', 'env_vars']
