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


]
