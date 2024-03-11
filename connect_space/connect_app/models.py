from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):

    user_object = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=200, null=True, blank=True)
    
    last_name = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(upload_to='images/profile_image/', default='images/default.jpg', null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    phone = models.CharField(max_length=10, null=True, blank=True)

    bio = models.CharField(max_length=200, null=True, blank=True)

    gender_choices = (

        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),

    )

    gender = models.CharField(max_length=150, choices=gender_choices, default='male')

    address = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user_object.username
    


    
    


class Post(models.Model):

    post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_owner')

    title = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(upload_to='images/post_image/', null=True, blank=True)

    content = models.TextField(null=True, blank=True)

    liked_by = models.ManyToManyField(User, related_name='likes', null=True, blank=True)

    disliked_by = models.ManyToManyField(User, related_name='dislikes', null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)


    class Meta:

        ordering = ['-created_date']



    @property
    def like_count(self):

        likes = self.liked_by.count()

        return likes
    

    @property
    def dislike_count(self):

        dislikes = self.disliked_by.count()

        return dislikes
    

    @property
    def comment_count(self):

        comments = self.comment_for_post.count()

        return comments
    


class Comment(models.Model):

    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_owner')

    post_object = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_for_post')

    comment_text = models.TextField(null=True, blank=True)
    
    comment_image = models.ImageField(upload_to='images/comment_image/', blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)


    

class Follow(models.Model):

    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name='following')

    follows = models.ManyToManyField(User, related_name='followers')

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)


    def __str__(self):

        return self.follower.username
    

    @property
    def following_count(self):

        following = self.follows.count()

        print(following)

        return following
    

    @property
    def follower_count(self):

        all_user = User.objects.all()

        all_followers = Follow.objects.all().filter(follows=self.follower).count()

        print(all_followers)

        return all_followers
    

    


   
    



# class Story(models.Model):

#     user_object = models.ForeignKey(User, on_delete=models.CASCADE)

#     image = models.ImageField(upload_to='images/story_image', null=True, blank=True)

#     video = models.FileField(upload_to='images/story_video/', null=True, blank=True)

#     text = models.CharField(max_length=300, null=True, blank=True)

#     created_date = models.DateTimeField(auto_now_add=True)

#     updated_date = models.DateTimeField(auto_now=True)

#     is_active = models.BooleanField(default=True)
    



def create_user_profile(sender, instance, created, **kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)



post_save.connect(sender=User, receiver=create_user_profile)




def create_follow_for_user(sender, instance, created, **kwargs):

    if created:

        Follow.objects.create(follower=instance)

    
post_save.connect(sender=User, receiver=create_follow_for_user)