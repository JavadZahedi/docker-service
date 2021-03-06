# Generated by Django 4.0 on 2022-01-03 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='image',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='keyvalue',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='env_vars', to='api.app'),
        ),
    ]
