from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^registration$', views.registration),
	url(r'^login$', views.user_login),
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^make_order$', views.make_order),
	url(r'^delete_order/(?P<id>\d+)$', views.delete_order),
	url(r'^admin_account$', views.admin_account),
	url(r'^delete_order_by_superuser/(?P<id>\d+)$', views.delete_order_by_superuser),
	url(r'^partner/(?P<id>\d+)$', views.partner),
]