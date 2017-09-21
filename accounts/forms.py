from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import re
from django.forms.models import inlineformset_factory
from smartfields import fields

from . import models


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.Skills
        fields = ['skills']


class UserProfileForm(forms.ModelForm):
    avatar = fields.ImageField(upload_to='avatars/', blank=True)
    bio = forms.CharField(max_length=150,
                          label='About Me',
                          required=False,
                          widget=forms.Textarea(),
                          min_length=5
                          )
    name = forms.CharField(label='Full Name')

    class Meta:
        model = models.Profile
        fields = [
            'name',
            'avatar',
            'bio',
        ]

SkillsFormSet = forms.modelformset_factory(
    models.Skills,
    form=SkillForm,
)

SkillsInlineFormSet = forms.inlineformset_factory(
    models.Profile,
    models.Skills,
    extra=1,
    fields=('skills',),
    formset=SkillsFormSet,
    min_num=1,
)
