# Generated by Django 4.2.1 on 2023-06-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_rename_post_content_post_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
