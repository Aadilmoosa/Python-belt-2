from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^create$', views.create),
    url(r'^add_favorite/(?P<id>\d+)$', views.add_favorite),
    url(r'^delete_favorite/(?P<id>\d+)$', views.delete_favorite),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^show_quote/(?P<quote_id>\d+)$', views.show_quote),
    ]