# Generated by Django 5.0.6 on 2024-06-10 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='friends_request_received',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='friends_request_sent',
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
