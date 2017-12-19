from django.conf.urls import url

from . import views

app_name = 'qanda'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^post/$', views.PostQuestionView.as_view(), name='post'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile')
]