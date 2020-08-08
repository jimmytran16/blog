
from django.contrib import admin
from django.urls import path
from . import views

#url mappings to the views functions
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('submit',views.register_submit,name='registerSubmit'),
    path('login',views.login,name='login'),
    path('loginUser',views.submit_login,name='submitLogin'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'), #user's dashboard
    path('home',views.dash_home,name='dashhome'), #home page of the user (when they log in)
    path('submitPost',views.submit_post,name='submitPost'), #post submission
    path('readPost',views.read_post,name='readPost'), #page to read a post
    path('settings',views.settings_page,name='settings_page'), #settings page of the user
    path('changeProfile/<int:id>',views.change_profile,name='changeProfile'), #passing the user id as an arguemnt into the path... to change the profile picture of the user
    path('usersPosts',views.usersPosts,name='usersPosts'), #shows all the posts of the users
    path('edit/<int:id>',views.edit_post,name='edit'), #edit the posts
    path('comfirmEdits/<int:id>',views.confirm_edits,name='comfirmEdits'), #comfirm the edits, passing in the post id as a parameter
    path('deletePost/<int:id>',views.delete_post,name='deletePost'), # maps to the function that will delete the post

    #settings edits
    path('settings/updatePassword',views.update_password,name='updatePassword'), #update your password from settings
    path('settings/updateInformation',views.update_setting_information,name='updateInformation'), #update your password from settings
]
