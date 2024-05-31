from django.shortcuts import render, redirect

from django.views.generic import View

from connect_app.forms import RegistrationForm, LoginForm, UserProfileForm, PostAddForm, CommentForm, FollowForm, StoryForm

from django.contrib.auth import authenticate, login, logout

from connect_app.models import UserProfile, Post, Comment, Follow, Story

from connect_app.decorators import signin_required

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from django.contrib import messages

from django.db.models import Count

from django.http import JsonResponse

from django.contrib.auth.models import User

import json

from django.core import serializers

from datetime import datetime, timedelta, timezone

from django.utils import timezone

# Create your views here.


class SignUpView(View):

    def get(self, request, *args, **kwargs):

        form = RegistrationForm()

        return render(request, 'register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST, files=request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created.")

            return redirect('signin')
        
        messages.error(request, "Error: Try again")
        
        return render(request, 'register.html', {'form': form})



class SignInView(View):

    def get(self, request, *args, **kwargs):

        form = LoginForm()

        return render(request, 'login.html', {'form':form})

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():

            uname = form.cleaned_data.get('username')

            pwd = form.cleaned_data.get('password')

            user_object = authenticate(request, username=uname, password=pwd)

            if user_object:

                login(request, user_object)

                return redirect('home')
        
        messages.error(request, "Error: Invalid credentials. Try again.")
            
        return render(request, 'login.html', {'form': form})
    

@method_decorator([signin_required, never_cache], name='dispatch')
class SignOutView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            logout(request)

        return redirect('signin')
    



@method_decorator([signin_required, never_cache], name='dispatch')
class HomeView(View):

    def get(self, request, *args, **kwargs):

        try:
            # user followers
            user_followers = Follow.objects.filter(follows=request.user)

            print(user_followers)

             # user following
            user_following = Follow.objects.get(follower=request.user).follows.all()

            print(user_following)


            all_user_profiles = UserProfile.objects.all()
       
            all_post_obj = Post.objects.all()

            all_comment_obj = Comment.objects.all()

        except:
            
            pass

        logged_in_user_post = Post.objects.filter(post_by=request.user)

        logged_in_user_post_count = logged_in_user_post.aggregate(total_post=Count('id')) 

        profile_obj = UserProfile.objects.get(user_object=request.user)



        try:
            # story delete of logged user if expired 

            logged_in_user_story = Story.objects.filter(user_object=request.user)

            for story in logged_in_user_story:

                print('updated',story.updated_date)

                story_updated_date = story.updated_date

                story_expiry_date = story_updated_date + timezone.timedelta(days=1)

                print('exp:', story_expiry_date)

                # now = datetime.today() # time naive object
                # print('today', now)

                # print('tommorrow', (now + timedelta(days=1)))

                # print(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

                # print('exp_date', (story_updated_date + timedelta(days=1)))

                # print(timezone.now() + timezone.timedelta(days=2))

                if story_expiry_date <= timezone.now() :

                    story.delete()  # logged user story delete

        except:
            
            pass

        

        # story of users followed by logged user
        users_with_story = {}

        user_profiles = UserProfile.objects.all().exclude(user_object=request.user)

        try: 

            admin_obj = User.objects.get(username='admin')

            user_profiles = user_profiles.exclude(user_object=admin_obj)

            for user in user_profiles:

                story_objects = user.user_object.story.filter(user_object=user.user_object)

                if story_objects and request.user.following.follows.contains(user.user_object):
                    
                    users_with_story.update({user.user_object : story_objects})

            # print(users_with_story)
                    
        except:

            pass


        return render(request, 'home.html', {

                                            'profile_obj': profile_obj,

                                            'all_post': all_post_obj,

                                            'post_count':logged_in_user_post_count,

                                            'user_profiles': all_user_profiles, 

                                            'user_following': user_following,
                                            
                                            'all_comments': all_comment_obj,

                                            'all_user_story': logged_in_user_story,

                                            'story_objects': users_with_story,
                                            
                                            'user_profiles': user_profiles,
                                            
                                            })

  
# comment view
@method_decorator([signin_required, never_cache], name='dispatch')
class CommentView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)
        
        all_comments = Comment.objects.all()

        comment_obj = Comment(comment_by=request.user, post_object=post_obj)

        form = CommentForm(instance=comment_obj)

        return render(request, 'comment_add.html', {'comment_form': form, 'post': post_obj, 'all_comments': all_comments})
    
  
    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        all_comments = Comment.objects.all()

        comment_obj = Comment(comment_by=request.user, post_object=post_obj)

        form = CommentForm(request.POST, files=request.FILES, instance=comment_obj)

        if form.is_valid():

            form.save()

            form = CommentForm()
            # return redirect('home')

        return render(request, 'comment_add.html', {'comment_form': form, 'post': post_obj, 'all_comments': all_comments})
    

# ajax comment add
    
# class CommentAddView(View):

#     def post(self, request, *args, **kwargs):
#         if request.is_ajax():
#             print(request.POST)
#         if request.POST.get('action') == 'post':

#             print(request.POST.get('formData'))


#             return JsonResponse({"message": "success"})



# ajax comment delete
class CommentDeleteView(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('action') == 'post':

            print(request.POST)
            id = int(request.POST.get('comment_id'))

            Comment.objects.get(id=id).delete()

            return JsonResponse({'msg':'success'})

 

# logged user profile view
@method_decorator([signin_required, never_cache], name='dispatch')
class ProfileView(View):

    def get(self, request, *args, **kwargs):

        profile_object = UserProfile.objects.get(user_object=request.user)

        form = UserProfileForm(instance=profile_object)

        return render(request, 'profile.html', {'form': form, 'profile_obj': profile_object})
    
    def post(self, request, *args, **kwargs):


        profile_object = UserProfile.objects.get(user_object=request.user)

        form = UserProfileForm(request.POST, files=request.FILES, instance=profile_object)

        if form.is_valid():

            form.save()

            messages.success(request, 'Profile updated.')

            return redirect('myprofile')

        
        messages.error(request, 'Profile not updated! Try again.')

        return render(request, 'profile.html', {'form': form})




# other user details view   
@method_decorator([signin_required, never_cache], name='dispatch')
class OtherUserDetailView(View):

     def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        data = UserProfile.objects.get(id=id)

        post_obj = Post.objects.filter(post_by=data.user_object)

        post_count = data.user_object.post_owner.all().count()

        print(post_count)

        comment_obj = Comment.objects.all()

        follow_obj = Follow.objects.get(follower=request.user)

        is_following = False

        if follow_obj.follows.contains(data.user_object):

            is_following = True


        return render(request, 'other_user_details.html', {
            
                                                            'profile_obj': data, 
                                                            'is_following': is_following, 
                                                            'post_obj':post_obj,
                                                            'all_comments': comment_obj,
                                                            'post_count': post_count,

                                                            })


        
# # follow user view (replaced with ajax)
# class FollowUserView(View):
    
#     def post(self, request, *args, **kwargs):

#         id = kwargs.get('pk')

#         follow_profile_obj = UserProfile.objects.get(id=id)

#         try:
        
#             follow_obj = Follow.objects.create(follower=request.user)

#             follow_obj.save()

#         except:

#             follow_obj = Follow.objects.get(follower=request.user)


#         follow_obj.follows.add(follow_profile_obj.user_object)

#         follow_obj.save()

#         return redirect('following-users')


# # unfollow users (replaced with ajax)
# class UnFollowUserView(View):

#     def post(self, request, *args, **kwargs):

#         id = kwargs.get('pk')

#         followed_by_user = UserProfile.objects.get(id=id)

#         follow_obj = Follow.objects.get(follower=request.user)

#         follow_obj.follows.remove(followed_by_user.user_object)

#         return redirect('following-users')
      


# follow other user
# ajax requests  
@method_decorator([signin_required, never_cache], name='dispatch')
class FollowOtherUserView(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('action') == 'post':

            user_id = request.POST.get('user_id')

            follow_user = User.objects.get(id=user_id)

            request.user.following.follows.add(follow_user)

            response = JsonResponse({'msg': 'following'})

            return response


# unfollow user
# ajax request    
@method_decorator([signin_required, never_cache], name='dispatch')    
class UnFollowOtherUserView(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('action') == 'post':

            user_id = request.POST.get('user_id')

            unfollow_user = User.objects.get(id=user_id)

            request.user.following.follows.remove(unfollow_user)

            response = JsonResponse({'msg': 'unfollowed'})

            return response




# all users in database except admin
@method_decorator([signin_required, never_cache], name='dispatch')
class AllUserView(View):

    def get(self, request, *args, **kwargs):

        all_users = User.objects.all().exclude(username='admin')

        login_following_users = Follow.objects.get(follower=request.user).follows.all()

        # print(login_following_users)

        login_user_followers = Follow.objects.filter(follows=request.user)

        # print(login_user_followers)

        return render(request, 'all_user.html', {'all_users': all_users, 'user_following': login_following_users})



# all following users
@method_decorator([signin_required, never_cache], name='dispatch')
class FollowingUsersView(View):

    def get(self, request, *args, **kwargs):

        login_following_users = Follow.objects.get(follower=request.user).follows.all()
        # print(login_following_users)

        return render(request, 'following_users.html', {'all_following': login_following_users})
    


# all followed users
@method_decorator([signin_required, never_cache], name='dispatch')
class FollowedUsersView(View):

    def get(self, request, *args, **kwargs):
        
        # login_user_followers = Follow.objects.all().filter(follows=request.user)

        login_user_followers = request.user.followers.all()
        # print(login_user_followers)

        # login_user_followers = Follow.objects.all().filter(follows=request.user)

        # print(login_user_followers)

        return render(request, 'followed_users.html', {'all_followed': login_user_followers})



@method_decorator([signin_required, never_cache], name='dispatch')
class PostAddView(View):

    def get(self, request, *args, **kwargs):

        post_obj = Post(post_by=request.user)

        form = PostAddForm(instance=post_obj)

        return render(request, 'post_add.html', {'form': form})

    def post(self, request, *args, **kwargs):

        post_obj = Post(post_by=request.user)

        form = PostAddForm(request.POST, files=request.FILES, instance=post_obj)

        if form.is_valid():

            form.save()

            return redirect('home')
        
        return render(request, 'post_add.html', {'form': form})


@method_decorator([signin_required, never_cache], name='dispatch')
class PostDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        Post.objects.get(id=id).delete()

        return redirect('home')
    

@method_decorator([signin_required, never_cache], name='dispatch')
class PostEditView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        all_comments = Comment.objects.all()

        form = PostAddForm(instance=post_obj)

        return render(request, 'post_edit.html', {'form':form, 'post': post_obj, 'all_comments': all_comments})
    

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        all_comments = Comment.objects.all()

        form = PostAddForm(request.POST, files=request.FILES, instance=post_obj)

        if form.is_valid():

            form.save()

            return redirect('home')
        
        return render(request, 'post_edit.html', {'form':form, 'post': post_obj, 'all_comments': all_comments})
    

# post like and dislike (normal)
@method_decorator([signin_required, never_cache], name='dispatch')
class PostLikeDislikeView(View):

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        # print(request.POST.get('like-dislike'))

        if post_obj.post_by == request.user and request.POST.get('like-dislike') == 'like':

            # print(post_obj.liked_by.all())

            # all_likes_list = post_obj.liked_by.all()

            return redirect('all-like-dislike')


        if post_obj.post_by != request.user:

            if post_obj.liked_by.contains(request.user) and request.POST.get('like-dislike') == 'like':

                user_object = request.user

                post_obj.liked_by.remove(user_object)

                return redirect('home')
            

            if post_obj.disliked_by.contains(request.user) and request.POST.get('like-dislike') == 'dislike':

                user_object = request.user

                post_obj.disliked_by.remove(user_object)

                return redirect('home')


            if request.POST.get('like-dislike') == 'like' and not post_obj.disliked_by.contains(request.user):

                user_object = request.user

                post_obj.liked_by.add(user_object)

            elif request.POST.get('like-dislike') == 'dislike' and not post_obj.liked_by.contains(request.user):

                user_object = request.user

                post_obj.disliked_by.add(user_object)

        post_obj.save()


        return redirect('home')



# like post with ajax  
@method_decorator([signin_required, never_cache], name='dispatch')
class PostLikeView(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('action') == 'post':

            post_id = request.POST.get('post_id')

            post_object = Post.objects.get(id=post_id)

            if post_object.disliked_by.contains(request.user):

                post_object.disliked_by.remove(request.user)


            if not post_object.liked_by.contains(request.user):

                post_object.liked_by.add(request.user)

                current_like_count = post_object.liked_by.all().count()

                current_dislike_count = post_object.disliked_by.all().count()

                response = JsonResponse({'msg': 'liked', 'like_count': current_like_count, 'dislike_count': current_dislike_count, 'post_id': post_id})

                return response
            
            elif post_object.liked_by.contains(request.user):

                post_object.liked_by.remove(request.user)

                current_like_count = post_object.liked_by.all().count()

                current_dislike_count = post_object.disliked_by.all().count()
                
                response = JsonResponse({'msg': 'like removed', 'like_count': current_like_count, 'dislike_count': current_dislike_count, 'post_id': post_id})

                return response
    
            
# ajax dilike   
@method_decorator([signin_required, never_cache], name='dispatch')       
class PostDislikeView(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('action') == 'post':

            post_id = request.POST.get('post_id')

            post_object = Post.objects.get(id=post_id)

            if post_object.liked_by.contains(request.user):

                post_object.liked_by.remove(request.user)

            if not post_object.disliked_by.contains(request.user):

                post_object.disliked_by.add(request.user)

                current_dislike_count = post_object.disliked_by.all().count()

                current_like_count = post_object.liked_by.all().count()

                response = JsonResponse({'msg': 'disliked', 'dislike_count': current_dislike_count, 'like_count': current_like_count, 'post_id': post_id})

                return response
            
            elif post_object.disliked_by.contains(request.user):
                
                post_object.disliked_by.remove(request.user)

                current_dislike_count = post_object.disliked_by.all().count()

                current_like_count = post_object.liked_by.all().count()

                response = JsonResponse({'msg': 'dislike removed', 'dislike_count': current_dislike_count, 'like_count': current_like_count, 'post_id': post_id})

                return response
                


@method_decorator([signin_required, never_cache], name='dispatch')
class LoggedInUserAllLikesDislikesView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        all_comments = Comment.objects.all()

        # print(request.GET.get('like-dislike'))

        action = request.GET.get('like-dislike')

        if request.GET.get('like-dislike') == 'like':

            all_user = post_obj.liked_by.all()

        elif request.GET.get('like-dislike') == 'dislike':

            all_user = post_obj.disliked_by.all()

        # print(all_user)

        return render(request, 'all_likes.html', {'all_user': all_user, 'action': action, 'post': post_obj, 'all_comments': all_comments})


# all post of user
@method_decorator([signin_required, never_cache], name='dispatch')
class MyPostsView(View):

    def get(self, request, *args, **kwargs):

        all_posts = Post.objects.filter(post_by=request.user)

        all_comments = Comment.objects.all()

        return render(request, 'my_post.html', {'all_posts': all_posts, 'all_comments': all_comments})
    

@method_decorator([signin_required, never_cache], name='dispatch')
class SearchPeopleView(View):

    def get(self, request, *args, **kwargs):

        search_text = ''
        if request.GET.get('action') == 'get':

            search_text = request.GET.get('search_text')
       
        # all_u = UserProfile.objects.filter(first_name__contains=search_text).exclude(first_name=request.user.profile.first_name) or UserProfile.objects.filter(last_name__startswith=search_text).exclude(last_name=request.user.profile.last_name)
        all_u = UserProfile.objects.filter(first_name__iexact=search_text).exclude(id=request.user.id) or UserProfile.objects.filter(last_name__iexact=search_text).exclude(id=request.user.id)

        data = serializers.serialize("json", list(all_u), fields=('first_name', 'last_name',))
        # print(data)

        # filter_result = json.dumps(data)

        # print(filter_result)

        response = JsonResponse({'success': 'success', 'data':data})

        return response



@method_decorator([signin_required, never_cache], name='dispatch')
class StoryView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        user_obj = User.objects.get(id=id)

        data = Story.objects.filter(user_object=user_obj)

        return render(request, 'story.html', {'all_user_story': data, 'user_obj': user_obj})



@method_decorator([signin_required, never_cache], name='dispatch')
class StoryAddView(View):

    def get(self, request, *args, **kwargs):

        story_object = Story(user_object=request.user)

        form = StoryForm(instance=story_object)

        return render(request, 'story_add.html', {'form': form})
    
    def post(sefl, request, *args, **kwargs):

        story_object = Story(user_object=request.user)

        form = StoryForm(request.POST, files=request.FILES, instance=story_object)

        if form.is_valid():

            form.save()

            return redirect('home')

        return render(request, 'story_add.html', {'form': form})
    

# edit story view
@method_decorator([signin_required, never_cache], name='dispatch')
class StoryEditView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        story_obj = Story.objects.get(id=id)

        form = StoryForm(instance=story_obj)

        return render(request, 'story_edit.html', {'form': form, 'story': story_obj})
    
    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        story_obj = Story.objects.get(id=id)

        form = StoryForm(request.POST, files=request.FILES, instance=story_obj)

        if form.is_valid():

            form.save()

            return redirect('home')
        
        return render(request, 'story_edit.html', {'form': form})


@method_decorator([signin_required, never_cache], name='dispatch')
class StoryDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        Story.objects.get(id=id).delete()

        return redirect('home')


