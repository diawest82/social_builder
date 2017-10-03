from django.test import TestCase, Client
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from .models import Projects, Positions, Applications
from .views import ProjectDetailView, ProjectDeleteView, create_project, edit_project
from . import forms


USER_DATA = {
    'username': 'tester',
    'email': 'test@test.com',
    'password': 'password',
}

PROJECT_DATA = {
    'title': 'Project Test',
    'description': 'test description',
    'time_estimate': '2 hours',
    'requirements': 'requirements test'
}

POSITION_DATA = {
    'name': 'Python Test',
    'description': 'test description'
}



class TestData(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(**USER_DATA)
        self.client = Client()
        self.project1 = Projects.objects.create(
            owner=self.user,
            title='New Proj Test',
            description='This project is a test',
            time_estimate='40 hours'
        )
        self.position = Positions.objects.create(
            project=self.project1,
            name='Python Developer',
            description='The info'
        )
        self.client.get(reverse('auth_login'))
        self.client.login(username='tester', password='password')

    def tearDown(self):
        self.user.delete()

#### Test Models ####
class ModelTest(TestCase):
    def test_project_model(self):
        User = get_user_model()
        self.user = User.objects.create_user(**USER_DATA)
        project = Projects.objects.create(
            owner=self.user,
            title='New Prj',
            description='This project is a test',
            time_estimate='40 hours'
        )
        self.assertEqual(project.title, 'New Prj')
        self.assertEqual(project.owner, self.user)

    def test_position_model(self):
        User = get_user_model()
        self.user = User.objects.create_user(**USER_DATA)
        project = Projects.objects.create(
            owner=self.user,
            title='New Prj',
            description='This project is a test',
            time_estimate='40 hours'
        )
        position = Positions.objects.create(
            project=project,
            name='Python Developer',
            description='The info'
        )
        self.assertEqual(position.name, 'Python Developer')

    def test_application_model(self):
        User = get_user_model()
        self.user = User.objects.create_user(**USER_DATA)
        project = Projects.objects.create(
            owner=self.user,
            title='New Prj',
            description='This project is a test',
            time_estimate='40 hours'
        )
        position = Positions.objects.create(
            project=project,
            name='Python Developer',
            description='The info'
        )

        application = Applications.objects.create(
            applicant=self.user,
            position=position,
        )
        self.assertEqual(application.position.name, 'Python Developer')


#### View Test ####
class TestView(TestData):
    def test_project_create(self):
        resp = self.client.get(reverse('projects:create_project'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_new.html')
        self.assertIsInstance(resp.context['form'], forms.ProjectForm)
        self.assertIsInstance(resp.context['formset'], forms.PositionInlineFormSet)
        resp = self.client.get(reverse('projects:create_project'),
            {'title': 'Project Test',
             'description': 'test description',
             'time_estimate': '2 hours',
             'requirements': 'requirements test'
             }
        )
        self.assertEqual(resp.status_code, 200)

    def test_edit_proj(self):
        resp = self.client.get(reverse('projects:project_edit',
                                       kwargs={
                                           'pk': self.project1.pk
                                       }),{
            'description': 'A better description',
            'time_estimate': '2 hours',
            'requirements': 'updated'
        }
                               )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_edit.html')

    def test_detail_view(self):
        resp = self.client.get(reverse('projects:detail',
                                       kwargs={
                                           'pk':self.project1.pk
                                       }
                                       ))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project.html')

    def test_delete_view(self):
        resp = self.client.get(reverse('projects:delete',
                                       kwargs={
                                           'pk': self.project1.pk
                                       }
                                       ))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_delete.html')
