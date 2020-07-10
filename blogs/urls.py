
from django.contrib import admin
from django.urls import path
from . import views

#url mappings to the views functions
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('submit',views.registerSubmit,name='registerSubmit'),
    path('login',views.login,name='login'),
    path('loginUser',views.submitLogin,name='submitLogin'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'), #user's dashboard
    path('home',views.dash_home,name='dashhome'), #home page of the user (when they log in)
    path('submitPost',views.submitPost,name='submitPost'), #post submission
    path('readPost',views.readPost,name='readPost'), #page to read a post
    path('settings',views.settingsPage,name='settingsPage'), #settings page of the user
    path('changeProfile/<int:id>',views.changeProfile,name='changeProfile'), #passing the user id as an arguemnt into the path... to change the profile picture of the user
    path('usersPosts',views.usersPosts,name='usersPosts'), #shows all the posts of the users
    path('edit/<int:id>',views.editPost,name='edit'), #edit the posts
    path('comfirmEdits/<int:id>',views.comfirmEdits,name='comfirmEdits'), #comfirm the edits, passing in the post id as a parameter
    path('deletePost/<int:id>',views.deletePost,name='deletePost'), # maps to the function that will delete the post

    #settings edits
    path('settings/updatePassword',views.updatePassword,name='updatePassword'), #update your password from settings
    path('settings/updateInformation',views.updateSettingsInformation,name='updateInformation'), #update your password from settings
]
