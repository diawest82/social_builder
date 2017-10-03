from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.


class Projects(models.Model):
    owner = models.ForeignKey(User, related_name='project', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    requirements = models.TextField(default='')
    time_estimate = models.TextField(default='')
    recruited = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    @property
    def open_positions(self):
        return self.positions.exclude(filled=True)

    def __str__(self):
        return self.title.title()

    def get_absoulute_url(self):
        return reverse('projects:project', kwargs={
            'project_id', self.id
        })


class Positions(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    filled = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name.title())

    def get_absolute_url(self):
        return self.project.get_absoulute_url()


class Applications(models.Model):
    applicant = models.ForeignKey(User, related_name='applicant')
    position = models.ForeignKey(Positions, related_name='applications')
    project = models.ForeignKey(Projects)
    is_accepted = models.NullBooleanField(default=None)

    def __str__(self):
        return '{} -- {} for {}'.format(self.applicant, self.position, self.project)


class ProjectSkills(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.CASCADE, related_name='skills')
    skills = models.CharField(max_length=25, default='')

    def __str__(self):
        return self.skills
