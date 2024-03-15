from django.urls import path

from connect_app import views

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='signup'),

    path('login/', views.SignInView.as_view(), name='signin'),

    path('', views.HomeView.as_view(), name='home'),

    path('logout/', views.SignOutView.as_view(), name='signout'),

    path('connect_space/profile/', views.ProfileView.as_view(), name='myprofile'),

    path('connect_space/post/add/', views.PostAddView.as_view(), name='post-add'),

    path('connect_space/post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post-delete'),

    path('connect_space/post/<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),

    path('connect_space/user/<int:pk>/', views.OtherUserDetailView.as_view(), name='other-user-detail'),

    path('connect_space/post/<int:pk>/like-dislike/', views.PostLikeDislikeView.as_view(), name='post-like-dislike'),

    path('connect_space/user-post/<int:pk>/all-like-dislike/', views.LoggedInUserAllLikesDislikesView.as_view(), name='all-like-dislike'),

    path('connect_space/post/<int:pk>/comment/add/', views.CommentView.as_view(), name='comment-add'),

    path('connect_space/user/<int:pk>/follow/', views.FollowUserView.as_view(), name='follow-user'),

    path('connect_space/user/<int:pk>/un-follow/', views.UnFollowUserView.as_view(), name='un-follow-user'),

    path('connect_space/all-users/', views.AllUserView.as_view(), name='all-user'),

    path('connect_space/users/following/', views.FollowingUsersView.as_view(), name='following-users'),

    path('connect_space/users/followers/', views.FollowedUsersView.as_view(), name='followed-users'),

    path('connect_space/users/posts/all/', views.MyPostsView.as_view(), name='my-posts'),

    # story view
    path('connect_space/story/add/', views.StoryView.as_view(), name='story-add'),

    path('connect_space/story/<int:pk>/remove/', views.StoryDeleteView.as_view(), name='story-delete'),

    path('connect_space/story/<int:pk>/change/', views.StoryEditView.as_view(), name='story-edit'),

    # search user
    path('search/', views.SearchPeopleView.as_view(), name='search-people'),

    # ajax unfollow

    path('unfollow/', views.UnFollowOtherUserView.as_view(), name='unfollow'),
    
    # ajax follow

    path('follow/', views.FollowOtherUserView.as_view(), name='follow'),

    # ajax like 

    path('like/', views.PostLikeView.as_view(), name='like'),

    # ajax dislike

    path('dislike/', views.PostDislikeView.as_view(), name='dislike'),
   

]
