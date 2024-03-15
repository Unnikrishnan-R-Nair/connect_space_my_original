from django.contrib import admin

from connect_app.models import UserProfile, Post, Comment, Follow, Story

# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Follow)

admin.site.register(Story)