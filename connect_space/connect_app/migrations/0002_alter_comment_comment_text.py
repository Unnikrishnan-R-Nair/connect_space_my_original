# Generated by Django 5.0.2 on 2024-03-12 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]