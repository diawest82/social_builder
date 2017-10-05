from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Q

from projects.models import *
from accounts.models import *

class Home(ListView):
    model = Projects
    template_name = 'index.html'
    context_object_name = 'project_home'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('s')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = self.kwargs.get('title')
        context['position'] = position
        context['skills'] = Profile.objects.get(user=self.request.user)
        return context


class JobFilter(ListView):
    model = Projects
    template_name = 'index_search.html'
    context_object_name = 'project_home'

    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.kwargs.get('title')
        queryset = queryset.filter(
            Q(positions__name__icontains=position)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = self.kwargs.get('title')
        context['position'] = position
        context['skills'] = Profile.objects.get(user=self.request.user)
        return context


class SkillFilter(ListView):
    model = Projects
    template_name = 'index_skills.html'
    context_object_name = 'project_home'

    def get_queryset(self):
        queryset = super().get_queryset()
        skills = self.kwargs.get('skill')
        queryset = queryset.filter(
            Q(positions__skills__skills__icontains=skills)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SkillFilter, self).get_context_data(**kwargs)
        skill = self.kwargs.get('skill')
        context['my_skills'] = Profile.objects.get(user=self.request.user)
        context['skills'] = skill
        return context


def job_filter(request, title):
    projects = Projects.objects.filter(__icontains=title.title)
    return render(request, 'index.html', {
        'project_home': projects
    })