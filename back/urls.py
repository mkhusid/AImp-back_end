import jwt_auth.views as jviews
from django.conf.urls import url, include


from . import views

app_name = 'back'



urlpatterns = [
    #url(r'^api-token-auth/$', jviews.obtain_jwt_token),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^signin/$', views.signin_view, name='signin'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^$', views.main, name='main'),
]
# url(r'^(?P<user_id>[0-9]+)/upload$', views.upload, name='upload'),

