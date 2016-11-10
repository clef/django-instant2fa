from django.conf.urls import url
import django.contrib.auth.views as auth_views
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_entrypoint, name='login'),
    url(r'^login/two-factor/$', views.two_factor_login, name='two_factor_login'),
    url(r'^login/two-factor-verification/$', views.two_factor_verification, name='two_factor_verification'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^user/settings', views.user_settings, name='user_settings')
]
