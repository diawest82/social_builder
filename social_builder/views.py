from django.views.generic import ListView
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


class CustomSearch(ListView):
    model = ProjectSkills
    template_name = 'index.html'
    context_object_name = 'project_home'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            project__title__icontains
        )

        return queryset
