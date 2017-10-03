from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin
from notifications.signals import notify
from projects.models import *
from . import models
from . import forms
# Create your views here.


STATUS_CHOICES ={
    'new': None,
    'accepted': True,
    'rejected': False
}


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    """Views User Profile"""
    template_name = 'accounts/profile.html'
    login_url = settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        lookup = kwargs.get('username')
        user = User.objects.filter(username=lookup)
        profile = models.Profile.objects.get(user=user)
        app = Applications.objects.filter(applicant=user)
        context['profile'] = profile
        context['skills'] = profile.skills_set.all()
        context['applications'] = app
        return context


@login_required
def edit_profile(request, pk):
    """ Edit User profile"""
    profile = get_object_or_404(models.Profile,
                                pk=pk)
    form = forms.UserProfileForm(instance=profile)
    skills_form = forms.SkillsInlineFormSet(
        queryset=form.instance.skills_set.all()
    )

    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST,
                                     instance=profile,
                                     files=request.FILES)
        skills_form = forms.SkillsInlineFormSet(
            request.POST,
            queryset=form.instance.skills_set.all(),
        )
        if form.is_valid() and skills_form.is_valid():
            form.save()
            skills = skills_form.save(commit=False)
            for skill in skills:
                skill.profile = profile
                skill.save()
            for skill in skills_form.deleted_objects:
                skill.delete()
            messages.success(request, 'Your profile has been updated!')
            return HttpResponseRedirect(reverse(
                'accounts:profile',
                kwargs={
                    'username': request.user.username
                }
            ))
    return render(request, 'accounts/profile_edit.html',
                  {
                      'form': form,
                      'form2': skills_form
                  })


class ProjectApplications(LoginRequiredMixin,
                          PrefetchRelatedMixin, generic.ListView):
    model = Applications
    template_name = 'accounts/applications.html'
    prefetch_related = ['project', 'position']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_term = self.request.GET.get('status') or 'all'

        if status_term and status_term != 'all':
            if status_term in STATUS_CHOICES.keys():
                queryset = queryset.filter(
                    is_accepted=STATUS_CHOICES[status_term]
                )
                return queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectApplications, self).get_context_data(**kwargs)
        applications = Applications.objects.all()
        projects = Projects.objects.prefetch_related(
            'positions').filter(owner=self.request.user)
        context['applications'] = applications.filter(~Q(
            applicant=self.request.user))
        context['projects'] = projects
        return context


class UserApplicationStatus(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        pos_pk = self.kwargs.get('position')
        position = Positions.objects.get(pk=pos_pk)
        if position.project.owner == self.request.user:
            applicat_pk = self.kwargs.get('applicant')
            applicant = get_object_or_404(User, pk=applicat_pk)
            status = self.kwargs.get('status')
            if status == 'approve' or status == 'deny':
                if position and applicant:
                    bstatus = True if status == 'approve' else False
                    application = Applications.objects.filter(
                        position=position, applicant=applicant
                    ).update(is_accepted=bstatus)

                    if status == 'approve':
                        msg_status = 'approved'
                    else:
                        msg_status = 'denied'

                    notify.send(
                        applicant,
                        recipient=applicant,
                        verb='Your application for {} as {} was {}'.format(
                            position.project.title, position.name, msg_status),
                        description=''
                    )
                    return HttpResponseRedirect(reverse('accounts:applications'))
        return HttpResponseRedirect(reverse('accounts:applications'))


class UserNotifications(LoginRequiredMixin,
                        PrefetchRelatedMixin, generic.TemplateView):
    template_name = 'accounts/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unreads'] = self.request.user.notifications.unread()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def search_applicants(request, status):
    if status in STATUS_CHOICES.keys():
        apps = Applications.objects.filter(is_accepted=STATUS_CHOICES[status])
    projects = Projects.objects.prefetch_related(
        'positions').filter(owner=request.user)
    return render(request, 'accounts/applications.html', {
        'applications': apps,
        'projects': projects
    })
