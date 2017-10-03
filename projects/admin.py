from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Positions)
admin.site.register(models.Projects)
admin.site.register(models.Applications)
admin.site.register(models.ProjectSkills)
