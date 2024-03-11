from django import forms 

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from connect_app.models import UserProfile, Post, Comment, Follow


class RegistrationForm(UserCreationForm):

    class Meta:

        model = User

        fields = ['username', 'email', 'password1', 'password2']

        
 
class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        exclude = ('created_date', 'updated_date', 'is_active','user_object',)


        
class PostAddForm(forms.ModelForm):

    class Meta:

        model = Post

        exclude = ('created_date', 'updated_date', 'is_active', 'post_by', 'liked_by', 'disliked_by',)


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        exclude = ('created_date', 'updated_date', 'is_active', 'comment_by', 'post_object',)



class FollowForm(forms.ModelForm):

    class Meta:

        model = Follow

        exclude = ('created_date', 'updated_date', 'is_active',)