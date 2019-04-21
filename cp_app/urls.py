from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root, name="index"),
    url(r'^add_user$', views.UserAdd.as_view()),
    url(r'^partners/$', views.PartnerList.as_view()),
    url(r'^partners/(\d+)$', views.partner_detail),
    url(r'^partners/delete/(\d+)$', views.partner_delete),
]