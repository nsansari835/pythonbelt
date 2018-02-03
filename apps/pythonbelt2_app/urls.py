from django.conf.urls import url
from . import views
from django.core.urlresolvers import reverse

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^add$', views.add),    
    url(r'^destination/(?P<id>\d+)$', views.show), 
    url(r'^addtrip$', views.addtrip),
    url(r'^join/(?P<id>\d+)$', views.join),    
    url(r'^logout', views.logout),
    url(r'^log', views.log),

]