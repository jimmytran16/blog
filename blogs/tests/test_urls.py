from django.test import SimpleTestCase
from django.urls import reverse,resolve
from blogs.views import *

# SimpleTestCase does not involve a DB
class TestTheBlogUrl(SimpleTestCase): #check if the url matches the module that django calls when the URL is exuecuted

    def test_home_page_is_resolved(self):
        url = reverse('home') #get the url path of the home request handler function
        self.assertEquals(resolve(url).func,home)

    def test_home_page_register_page_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func,register)

    def test_submit_page_is_resolved(self):
        url = reverse('registerSubmit')
        self.assertEquals(resolve(url).func,registerSubmit)

    def test_login_page_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,login)

    def test_login_user_page_is_resolved(self):
        url = reverse('submitLogin')
        self.assertEquals(resolve(url).func,submitLogin)

    def test_logout_page_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func,logout)

    def test_dashboard_page_is_resolved(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func,dashboard)

    def test_dash_home_page_is_resolved(self):
        url = reverse('dashhome')
        self.assertEquals(resolve(url).func,dash_home)

    def test_submit_post_is_resolved(self):
        url = reverse('submitPost')
        self.assertEquals(resolve(url).func,submitPost)

    def test_read_post_page_is_resolved(self):
        url = reverse('readPost')
        self.assertEquals(resolve(url).func,readPost)

    def test_settings_page_is_resolved(self):
        url = reverse('settingsPage')
        self.assertEquals(resolve(url).func,settingsPage)

    def test_user_post_is_resolved(self):
        url = reverse('usersPosts')
        self.assertEquals(resolve(url).func,usersPosts)

    # URLS with arguemnts passed

    def test_change_profile_is_resolved(self):
        context = {'some-int':[43]} # a list of existing posts from the database
        url = reverse('changeProfile',args=context['some-int'])
        self.assertEquals(resolve(url).func,changeProfile)

    def test_edit_is_resolved(self):
        context = {'some-int':[43]}
        url = reverse('edit',args=context['some-int'])
        self.assertEquals(resolve(url).func,editPost)

    def test_comfirm_edits_resolved(self):
        context = {'some-int':[43]}
        url = reverse('comfirmEdits',args=context['some-int'])
        self.assertEquals(resolve(url).func,comfirmEdits)

    def test_delete_post_is_resolved(self):
        context = {'some-int':[43]}
        url = reverse('deletePost',args=context['some-int'])
        self.assertEquals(resolve(url).func,deletePost)
