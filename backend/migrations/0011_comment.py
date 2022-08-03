# Generated by Django 4.0.6 on 2022-08-01 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0010_topic_wide_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('body', models.CharField(max_length=255)),
                ('time', models.DateTimeField(null=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
