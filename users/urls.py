from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
	path('signup/', views.CustomUserSignupView, name='custom_user_signup'),
	path('profile/edit/', views.EditProfileView, name='editprofile'),	
	path('manage/', views.ManageUserView, name='manage_users'),	
	path('lock-screen/', views.LockScreenView, name ='lockscreen'),
	path('profile/', views.CustomUserProfileCreationView, name='custom_user_profile'),
	path('login/', views.LoginView, name='login'),
	path('logout/', views.LogoutView, name='logout'),
]
