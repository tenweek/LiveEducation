from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^Hello', views.getVerification),
    url(r'^get-test', views.get_test),
    url(r'^SignUp', views.signUp),
    url(r'^Login', views.login),
]