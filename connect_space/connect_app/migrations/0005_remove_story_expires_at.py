# Generated by Django 5.0.2 on 2024-03-14 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect_app', '0004_alter_story_user_object'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='expires_at',
        ),
    ]
