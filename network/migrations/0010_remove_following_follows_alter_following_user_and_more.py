# Generated by Django 4.2.1 on 2023-06-26 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_rename_followedby_following_follows_following_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='follows',
        ),
        migrations.AlterField(
            model_name='following',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='following',
            name='follows',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]