from django.test import TestCase, Client
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from .models import User, Profile, Skills
from .forms import UserProfileForm, SkillsInlineFormSet

# Create your tests here.

USER_CREATE_DATA = {
    'username': 'tester',
    'email': 'test@gmail.com',
    'password': 'testpassword',
}

USER_Profile_Data = {
    'name': 'Tester',
    'bio': 'This is good'
}

SKILLS_DATA = {
    'skills': "python",
}


class TestData(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(**USER_CREATE_DATA)

        self.client = Client()

    def tearDown(self):
        self.user1.delete()


##### TestViews #####
class TestViews(TestData):
    def test_userprofile(self):
        resp = self.client.get(reverse('auth_login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/login.html')
        self.client.login(username='tester', password='testpassword')
        resp = self.client.get(reverse('accounts:profile',
                                       kwargs={
                                           'username': 'tester'
                                       }))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile.html')

    def test_userprofile_edit(self):
        resp = self.client.get(reverse('auth_login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/login.html')
        self.client.login(username='tester', password='testpassword')

        resp = self.client.get(reverse('accounts:edit_profile',
                                       kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile_edit.html')
        self.assertIsInstance(resp.context['form'], UserProfileForm)
        self.assertIsInstance(resp.context['form2'], SkillsInlineFormSet)
        resp = self.client.get(reverse('accounts:edit_profile',
                                       kwargs={'pk': 1}),
                               {
                                   'name': 'Tester',
                                   'bio': 'this is it',
                                   'skills': 'html'
                               }
                               )
        self.assertEqual(resp.status_code, 200)


#### Form Test ####
class FormTest(TestData):
    def test_profile_form(self):
        form = UserProfileForm(data={
            'name': 'Tester',
            'bio': 'This is me'
        })
        self.assertTrue(form.is_valid())
