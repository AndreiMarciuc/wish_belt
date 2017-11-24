from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main), 
    url(r'^main$', views.index), 
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    # url(r'^homepage$',views.dashboard),
    url(r'^logout$', views.logout),
]
