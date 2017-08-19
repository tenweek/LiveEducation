from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^createRoom/$', views.createRoom),
    url(r'^getRooms/$', views.getRooms),
    url(r'^getVerification/$', views.getVerification),
    url(r'^signUp/$', views.signUp),
    url(r'^login/$', views.login),
    url(r'^getRand/$', views.getRand),
    url(r'^changePasswd/$', views.changePasswd),
    url(r'^changeName/$', views.changeName),
    url(r'^getName/$', views.getName),
    url(r'^joinRoom/$', views.joinRoom),
    url(r'^getRoomInfo/$', views.getRoomInfo),
    url(r'^gag/$', views.gag),
    url(r'^checkGag/$', views.checkGag),
    url(r'^gagAll/$', views.gagAll),
    url(r'^allowSpeak/$', views.allowSpeak),
    url(r'^allowAllSpeak/$', views.allowAllSpeak),
    url(r'^kickOut/$', views.kickOut),
    url(r'^changeNum/$', views.changeNum),
    url(r'^upload/$', views.upload),
    url(r'^uploadFile/$', views.uploadFile),
    url(r'^getImg/$', views.getImg),
    url(r'^getTeacherFileInfo/$', views.getTeacherFileInfo),
    url(r'^closeLiveRoom/$', views.closeLiveRoom),
    url(r'^getVideoRooms/$', views.getVideoRooms)
]
