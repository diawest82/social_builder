from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import (authenticate,)
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings

from braces.views import LoginRequiredMixin
from . import models
from . import forms
# Create your views here.


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    """Views User Profile"""
    template_name = 'accounts/profile.html'
    login_url = settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        lookup = kwargs.get('username')
        user = User.objects.get(username=lookup)
        profile = models.Profile.objects.get(user=user)
        context['profile'] = profile
        context['skills'] = profile.skills_set.all()
        return context


"""class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    template_name = 'accounts/profile_edit.html'
    form_class = forms.UserProfileForm

    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        profile = models.Profile.objects.prefetch_related('skills_set').get(
            pk=self.object.pk)
        form2 = self.form_class(instance=profile)
        return render(request, 'accounts/profile_edit.html',
                      {
                          'profile': profile,
                          'form2': form2
                      }
                      )

    def get_success_url(self):
        messages.success(self.request, "Your Profile has been updated")
        return reverse(
            'accounts:profile',
            kwargs={'username': self.request.user.username}
        )"""



class UserProfileSkillsUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """Updates User Profile"""
    model = models.Profile
    template_name = 'accounts/profile_edit.html'
    form_class = forms.SkillsInlineFormSet
    form_class2 = forms.UserProfileForm

    def get_context_data(self, **kwargs):
        data = super(UserProfileSkillsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skills'] = forms.SkillsInlineFormSet(
                self.request.POST,
                instance=self.object
            )
            data['profile'] = forms.UserProfileForm(
                self.request.POST,
                instance=self.object
            )
        else:
            data['skills'] = forms.SkillsInlineFormSet(instance=self.object)
            data['profile'] = forms.UserProfileForm(
                instance=self.object
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context['skills']
        profile = context['profile']
        profile = form2.save(commit=False)
        profile.save()
        with transaction.atomic():
            self.object = form.save()

            if skills.is_valid():
                skills.instance = self.object
                skills.save()
        return super(UserProfileSkillsUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Your Profile has been updated")
        return reverse(
            'accounts:profile',
            kwargs={'username': self.request.user.username}
        )


class UserSkillsView(LoginRequiredMixin, generic.CreateView, generic.UpdateView):
    model = get_user_model()
    success_url = 'accounts/profile_edit.html'

    def get_context_data(self, **kwargs):
        data = super(UserSkillsView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skills'] = forms.UserSkillsFormSet(self.request.POST)
        else:
            data['skills'] = forms.UserSkillsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        skills = context['skills']
        with transaction.atomic():
            self.object = form.save()

            if skills.is_valid():
                skills.instance = self.object
                skills.save()
        return super(UserSkillsView, self).form_valid(form)



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
            #files=request.FILES
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
