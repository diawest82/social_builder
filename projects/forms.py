from django import forms
from django.forms.models import inlineformset_factory

from . import models


class ProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=150,
                            label='Project Title'
                            )
    description = forms.CharField(widget=forms.Textarea(),
                                  min_length=5
                                  )
    requirements = forms.CharField(widget=forms.Textarea(),
                                   min_length=5
                                   )
    time_estimate = forms.CharField(
        widget=forms.Textarea(
        attrs={'placeholder': 'Time estimate', 'class': 'circle--textarea--input'}
        ),
        required=False,
    )

    class Meta:
        model = models.Projects
        fields = [
            'title',
            'description',
            'requirements',
            'time_estimate'
        ]


class PositionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(),

    )

    class Meta:
        model = models.Positions
        fields = [
            'name',
            'description'
        ]


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.ProjectSkills
        fields = ['skills']


PositionFormSet = forms.modelformset_factory(
    models.Positions,
    form=PositionForm
)

PositionInlineFormSet = inlineformset_factory(
    models.Projects,
    models.Positions,
    formset=PositionFormSet,
    fields=['name', 'description'],
    can_delete=True,
    extra=1,
)

SkillsFormSet = forms.modelformset_factory(
    models.ProjectSkills,
    form=SkillForm,
)

SkillsInlineFormSet = inlineformset_factory(
    models.Positions,
    models.ProjectSkills,
    extra=1,
    fields=('skills',),
    formset=SkillsFormSet,
    can_delete=True
)