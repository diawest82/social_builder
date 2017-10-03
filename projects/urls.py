from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^my_projects/$', views.ProjectsListView.as_view(), name='my_projects'),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detail'),
    url(r'^apply/(?P<pk>\d+)/$', views.ApplyPositionView.as_view(), name='position_apply'),
    url(r'^create/$', views.ProjectCreateView.as_view(), name='create_project'),
    url(r'^edit/(?P<pk>\d+)/$', views.ProjectEditVIew.as_view(), name='project_edit'),
    url(r'^create_position/(?P<project_pk>\d+)/$', views.create_position, name='create_position'),
    url(r'^edit_position/(?P<project_pk>\d+)/(?P<position_pk>\d+)/$', views.edit_position, name='edit_position'),
    url(r'^delete/(?P<pk>\d+)/$', views.ProjectDeleteView.as_view(), name='delete'),
]
