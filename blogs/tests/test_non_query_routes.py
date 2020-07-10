from django.test import SimpleTestCase,Client
from django.urls import reverse


class test_non_queried_routes(SimpleTestCase):

    def setUp(self): # this function will be invoked when the instance is called
        self.status = 200 #set the status to be 200
        self.redirect_code = 302
        self.client = Client() #call an instance of a client
        self.mock_arg = [5]
        self.page_not_found_code = 404

    #this will check if the register handler will return a 200 response
    def test_register_page_response_code(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code,self.status)

    def test_login_page_response_code(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code,self.status)


    #Restrictued pages that should return 302 status -- users who are not logged in are prohibited from these requests
    def test_dashboard_page_response_code(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_settings_page_response_code(self):
        response = self.client.get(reverse('settingsPage'))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_users_home_page_response_code(self):
        response = self.client.get(reverse('dashhome'))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_users_edit_post_response_code(self):
        a = self.mock_arg # set up a mock arugument to pass into the parameter
        response = self.client.get(reverse('edit',args=a))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_users_change_profile_pic_response_code(self):
        a = self.mock_arg # set up a mock arugument to pass into the parameter
        response = self.client.get(reverse('changeProfile',args=a))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_delete_post_response_code(self):
        a = self.mock_arg
        response = self.client.get(reverse('deletePost',args=a))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_comfirm_edits_of_post_response_code(self):
        a = self.mock_arg
        response = self.client.get(reverse('comfirmEdits',args=a))
        self.assertEquals(response.status_code,self.redirect_code)

    def test_comfirm_edits_of_post_response_code(self):
        a = self.mock_arg
        response = self.client.get(reverse('deletePost',args=a))
        self.assertEquals(response.status_code,self.redirect_code)


    #updates - check if the content on the response has the word error in it
    #GET request for updatePassword,submitPost,updateInformation VIEWS -- should return 200 status code, but have specified content

    def test_update_password_content_check(self):
        response = self.client.get(reverse('updatePassword'))
        self.assertIn('Error',response.content.decode('utf-8'))

    def test_update_information_content_check(self):
        response = self.client.get(reverse('updateInformation'))
        self.assertIn('error',response.content.decode('utf-8'))

    def test_submit_post_get_request_content(self):
        response = self.client.get(reverse('submitPost'))
        self.assertIn('Error',response.content.decode('utf-8'))



    # def test_update_pass_post_request_content(self):
    #     response = self.client.post(reverse('updatePassword'))
    #     self.assertEquals(response.status_code,self.page_not_found_code)

    # def test_submit_post_post_request_content(self):
    #     response = self.client.post(reverse('submitPost'))
    #     self.assertEquals(response.status_code,self.page_not_found_code)

    # def test_update_info_post_request_content(self):
    #     response = self.client.post(reverse('updateInformation'))
    #     self.assertEquals(response.status_code,self.page_not_found_code)
