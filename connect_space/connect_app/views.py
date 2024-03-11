from django.shortcuts import render, redirect

from django.views.generic import View

from connect_app.forms import RegistrationForm, LoginForm, UserProfileForm, PostAddForm, CommentForm, FollowForm

from django.contrib.auth import authenticate, login, logout

from connect_app.models import UserProfile, Post, Comment, Follow

from connect_app.decorators import signin_required

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from django.contrib import messages

from django.db.models import Count

from django.http import JsonResponse

from django.contrib.auth.models import User

# Create your views here.

class SignUpView(View):

    def get(self, request, *args, **kwargs):

        form = RegistrationForm()

        return render(request, 'register.html', {'form': form})
    
    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST, files=request.FILES)

        if form.is_valid():

            form.save()

            return redirect('signin')
        
        return render(request, 'register.html', {'form': form})




@method_decorator([signin_required, never_cache], name='dispatch')
class HomeView(View):

    def get(self, request, *args, **kwargs):

        #profile
        # post
        # following
        # Story
        # comment

        all_user_profiles = UserProfile.objects.all()

        profile_obj = UserProfile.objects.get(user_object=request.user)

        all_post_obj = Post.objects.all()

        #print(all_post_obj)
 
        logged_in_user_post = Post.objects.filter(post_by=request.user)

        logged_in_user_post_count = logged_in_user_post.aggregate(total_post=Count('id'))  

        # each_post = all_post_obj.annotate(each_post=Count('id'))

        # print(each_post)

        # post_like_dict = {} 

        # for p in all_post_obj:

        #     print(p.liked_by.aggregate(likes=Count('id')))

        #     post_like_dict[p.id] = p.liked_by.aggregate(likes=Count('id'))

        # print(post_like_dict)

        # print(logged_in_user_post_count ) 


        # Comment

        # comment_obj1 = Comment(comment_by=request.user, post_object=Post.objects.get(id=2))

        all_comment_obj = Comment.objects.all()

        # comment_form = CommentForm(instance=comment_obj1)

        return render(request, 'home.html',{

                                            'profile_obj': profile_obj,
                                            'all_post': all_post_obj,
                                            'post_count':logged_in_user_post_count,
                                            'user_profiles': all_user_profiles, 
                                            # 'comment_form': comment_form,
                                            'all_comments': all_comment_obj,
                                            })

# comment view
class CommentView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)
        
        comment_by = request.user

        all_comments = Comment.objects.all()

        comment_obj = Comment(comment_by=request.user, post_object=post_obj)

        form = CommentForm(instance=comment_obj)

        return render(request, 'comment_add.html', {'comment_form': form, 'post': post_obj, 'all_comments': all_comments})
    
  
    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        comment_by = request.user

        all_comments = Comment.objects.all()

        comment_obj = Comment(comment_by=request.user, post_object=post_obj)

        form = CommentForm(request.POST, files=request.FILES, instance=comment_obj)

        if form.is_valid():

            form.save()

            return redirect('home')

        return render(request, 'comment_add.html', {'comment_form': form, 'post': post_obj, 'all_comments': all_comments})


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
            
        return render(request, 'login.html', {'form': form})
    


class SignOutView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            logout(request)

        return redirect('signin')
    


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
    
class OtherUserDetailView(View):

     def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        data = UserProfile.objects.get(id=id)

        try:

            follow_obj = Follow.objects.get(follower=request.user)
        
        except:

            follow_obj = Follow.objects.create(follower=request.user)

            follow_obj.save()


        is_following = False

        if follow_obj.follows.contains(data.user_object):

            is_following = True


        return render(request, 'other_user_details.html', {'data': data, 'is_following': is_following})
  
        

class FollowUserView(View):
    
    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        follow_profile_obj = UserProfile.objects.get(id=id)

        try:
        
            follow_obj = Follow.objects.create(follower=request.user)

            follow_obj.save()

        except:

            follow_obj = Follow.objects.get(follower=request.user)


        follow_obj.follows.add(follow_profile_obj.user_object)

        follow_obj.save()

        return redirect('following-users')


class UnFollowUserView(View):

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        followed_by_user = UserProfile.objects.get(id=id)

        follow_obj = Follow.objects.get(follower=request.user)

        follow_obj.follows.remove(followed_by_user.user_object)

        return redirect('following-users')
    


# all users in database except admin
class AllUserView(View):

    def get(self, request, *args, **kwargs):

        all_users = User.objects.all().exclude(username='admin')

        login_following_users = Follow.objects.get(follower=request.user).follows.all()

        print(login_following_users)

        login_user_followers = Follow.objects.filter(follows=request.user)

        print(login_user_followers)

        return render(request, 'all_user.html', {'all_users': all_users})



# all following users
class FollowingUsersView(View):

    def get(self, request, *args, **kwargs):

        try:

            login_following_users = Follow.objects.get(follower=request.user).follows.all()

        except:

            follow_obj = Follow.objects.create(follower=request.user)

            follow_obj.save()

            login_following_users = Follow.objects.get(follower=request.user).follows.all()


        print(login_following_users)

        return render(request, 'following_users.html', {'all_following': login_following_users})
    


# all followed users
class FollowedUsersView(View):

    def get(self, request, *args, **kwargs):

         

        try:

            # login_user_followers = Follow.objects.all().filter(follows=request.user)

            login_user_followers = request.user.followers.all()
            print(login_user_followers)

        except:
            
            follow_obj = Follow.objects.create(follower=request.user)

            follow_obj.save()

            # login_user_followers = Follow.objects.all().filter(follows=request.user)


        # print(login_user_followers)

        return render(request, 'followed_users.html', {'all_followed': login_user_followers})



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



class PostDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        Post.objects.get(id=id).delete()

        return redirect('home')
    


class PostEditView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        form = PostAddForm(instance=post_obj)

        return render(request, 'post_edit.html', {'form':form})
    

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        form = PostAddForm(request.POST, files=request.FILES, instance=post_obj)

        if form.is_valid():

            form.save()

            return redirect('home')
        
        return render(request, 'post_edit.html', {'form':form})
    

# post like and dislike
class PostLikeDislikeView(View):

    def post(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        post_obj = Post.objects.get(id=id)

        print(request.POST.get('like-dislike'))

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
class MyPostsView(View):

    def get(self, request, *args, **kwargs):

        all_posts = Post.objects.filter(post_by=request.user)

        all_comments = Comment.objects.all()

        return render(request, 'my_post.html', {'all_posts': all_posts, 'all_comments': all_comments})
    


# search people   

class SearchPeopleView(View):

    def post(self, request, *args, **kwargs):

        profile_obj = UserProfile.objects.get(first_name__icontains=request.post)

        return redirect('home')



