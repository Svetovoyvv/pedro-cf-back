from django.urls import path, re_path

from applications.gauth.api import views

urlpatterns = [
    re_path(r'^login/$', views.CustomLoginView.as_view(), name='login'),
    re_path(r'^user/$', views.CustomUserDetailsView.as_view(), name='user'),
]
