from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    # url(r'^Hello', views.get_test),
    url(r'^make-room', views.make_room),
    url(r'^list-room', views.list_room),
    url(r'^getVerification', views.getVerification),
    url(r'^SignUp', views.signUp),
    url(r'^Login', views.login),
    url(r'^getRand', views.getRand),
    url(r'^changePasswd', views.changePasswd),
    url(r'^changeName', views.changeName)
]
