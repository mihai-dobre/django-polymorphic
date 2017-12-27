from django.conf.urls import url, include
from django.contrib.auth.views import logout, LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from backend.apps.base.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='base/login.html') , name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', login_required(home), name='home'),
]
