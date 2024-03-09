# Generated by Django 5.0.2 on 2024-03-09 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect_app', '0006_alter_post_options_alter_comment_comment_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_for_post', to='connect_app.post'),
        ),
    ]
