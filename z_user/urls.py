from django.conf.urls import url
from z_user import views


urlpatterns = [
    url(r'^relogin/$', views.relogin),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^info/$', views.info),
    url(r'^user_center', views.user_center),
    url(r'^publish', views.publish)
]