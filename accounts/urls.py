from django.conf.urls import url, include

from . import views


urlpatterns = [
    #url(r'^$', views.user_profile, name='profile'),
   # url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)$', views.UserProfileView.as_view(), name='profile'),
    url(r'^edit/(?P<pk>\d+)$', views.edit_profile, name='edit_profile'),
    url(r'^applications/$', views.ProjectApplications.as_view(), name='applications'),
    url(r'^me/notifications/$', views.UserNotifications.as_view(), name='my_notifications'),
    url(
        r'^applications/(?P<position>[a-zA-Z0-9_]+)/(?P<applicant>\d+)/(?P<status>\w+)/$',
        views.UserApplicationStatus.as_view(), name='status_update'),
    url(r'^applications/(?P<status>[a-z,A-z\s]+)/$', views.search_applicants, name='status')
]
