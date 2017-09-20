from django.conf.urls import url, include

from . import views


urlpatterns = [
    #url(r'^$', views.user_profile, name='profile'),
   # url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)$', views.UserProfileView.as_view(), name='profile'),
    url(r'^edit/(?P<pk>\d+)$', views.edit_profile, name='edit_profile'),
]
