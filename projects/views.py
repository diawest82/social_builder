from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.contrib.auth.decorators import login_required
from notifications.signals import notify

from braces.views import LoginRequiredMixin
from . import models
from . import forms

# Create your views here.
class ProjectEditVIew(LoginRequiredMixin, generic.UpdateView):
    model = models.Projects
    form_class = forms.ProjectForm
    template_name = 'projects/project_edit.html'
    #context_object_name = 'project'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


@login_required
def edit_project(request, pk):
    """ Edit User profile"""
    project = get_object_or_404(models.Projects,
                                pk=pk)
    form = forms.ProjectForm(instance=project)
    formset = forms.PositionInlineFormSet(
        queryset=form.instance.positions.all()
    )

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST,
                                 instance=project,)
        formset = forms.PositionInlineFormSet(
            request.POST,
            queryset=form.instance.positions.all(),
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            positions = formset.save(commit=False)
            for position in positions:
                position.project = project
                position.save()
            for position in formset.deleted_objects:
                position.delete()
            messages.success(request, 'Your project has been updated!')
            return HttpResponseRedirect(reverse(
                'home'
            ))
    return render(request, 'projects/project_edit.html',
                  {'project': project,
                   'form': form,
                   'formset': formset
                   })


@login_required
def edit_position(request, project_pk, position_pk):
    """ Edit User profile"""
    position = get_object_or_404(models.Positions,
                                 pk=position_pk,
                                 project_id=project_pk)
    form = forms.PositionForm(instance=position)
    formset = forms.SkillsInlineFormSet(
        queryset=form.instance.skills.all()
    )

    if request.method == 'POST':
        form = forms.PositionForm(request.POST,
                                  instance=position,)
        formset = forms.SkillsInlineFormSet(
            request.POST,
            queryset=form.instance.skills.all(),
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            skills = formset.save(commit=False)
            for skill in skills:
                skill.position = position
                skill.save()
            for skill in formset.deleted_objects:
                skill.delete()
            messages.success(request, 'Your project has been updated!')
            return HttpResponseRedirect(reverse(
                'projects:detail', kwargs={
                    'pk': project_pk
                }
            ))
    return render(request, 'projects/position_edit.html',
                  {'position': position,
                   'form': form,
                   'formset': formset
                   })


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Projects
    template_name = 'projects/project_delete.html'
    context_object_name = 'project'
    form_class = forms.ProjectForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class ProjectDetailView(generic.DetailView):
    model = models.Projects
    context_object_name = 'project'
    template_name = 'projects/project.html'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Projects
    form_class = forms.ProjectForm
    context_object_name = 'project'
    template_name = 'projects/project_new.html'
    success_url = 'projects:my_projects'

    def post(self, request, *args, **kwargs):
        form = forms.ProjectForm(self.request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = self.request.user
            project.save()
        return HttpResponseRedirect(reverse(
            'projects:detail', kwargs={
                'pk': project.pk
            }
        ))


class ProjectsListView(LoginRequiredMixin, generic.ListView):
    model = models.Projects
    template_name = 'projects/my_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


@login_required
def create_position(request, project_pk):
    project = get_object_or_404(models.Projects, pk=project_pk)
    form = forms.PositionForm()
    skills_form = forms.SkillsInlineFormSet(
        queryset=models.ProjectSkills.objects.none()
    )

    if request.method == 'POST':
        form = forms.PositionForm(request.POST)
        skills_form = forms.SkillsInlineFormSet(
            request.POST,
            queryset=models.ProjectSkills.objects.none()
        )

        if form.is_valid() and skills_form.is_valid():
            position = form.save(commit=False)
            position.project = project
            position.save()
            skills = skills_form.save(commit=False)
            for skill in skills:
                skill.position = position
                skill.save()
            messages.success(request, "Added a new Position")
            return HttpResponseRedirect(reverse('projects:detail', kwargs={
                'pk': project_pk
            }))
    return render(request, 'projects/position_new.html', {
        'project': project,
        'form': form,
        'formset': skills_form
    })


class ApplyPositionView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        position = get_object_or_404(models.Positions, pk=pk)
        project = models.Projects.objects.get(title=position.project.title)
        application = models.Applications.objects.filter(
            position=position,
            applicant=self.request.user
        )
        if application.exists():
            messages.success(request, "You've already applied for this position!")
            return HttpResponseRedirect(reverse(
                'projects:project_detail', kwargs={'pk': pk}
            ))

        models.Applications.objects.create(
            applicant=self.request.user,
            project=project,
            position=position
        )

        notify.send(
            self.request.user,
            recipient=self.request.user,
            verb="You successfully submitted an application for {} as {}.".format(
                project.title, position.name
            ),
            description=''
        )
        notify.send(
            project.owner,
            recipient=project.owner,
            verb='{} submitted an application for {} as {}'.format(
                self.request.user, project.title, position.name
            ),
            description=''
        )
        return HttpResponseRedirect(reverse('home'))
