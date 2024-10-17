from django.urls import path
from user_auth.views import PasswordResetView, UserLoginView, UserRegistrationView , UserListView  , UserUpdateProfileView ,     UserRoleCountView
# UserProfileUpdateView


urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='signin'),
    # path('sociallogin/',SocialLoginView.as_view() , name="SocialLoginView"),
    path('reset-password', PasswordResetView.as_view(), name='reset-password'),


    path('users', UserListView.as_view(), name='user-list'),

    path('update-profile/<int:user_id>/', UserUpdateProfileView.as_view(), name='update-profile'),

    # path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update')
    # ,

    path('api/user/role-counts/', UserRoleCountView.as_view(), name='user-role-counts'),
    
]