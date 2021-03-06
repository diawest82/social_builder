"""social_builder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^jobs/(?P<title>[a-zA-Z0-9_" "]+)$', views.JobFilter.as_view(), name='jobs'),
    url(r'^skills/(?P<skill>[a-zA-Z0-9_" "]+)$', views.SkillFilter.as_view(), name='skills'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('accounts.urls', namespace='accounts')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^avatar/', include('avatar.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
