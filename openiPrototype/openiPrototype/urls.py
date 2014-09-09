from django.conf.urls import patterns, include, url

from django.contrib import admin
from appUI import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openiPrototype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^welcome$', views.getRecPlaces, name='welcome'),
    url(r'^index$', views.welcome, name='welcome'),
    url(r'^login', views.signin, name='login'),
    url(r'^logout', views.signout, name='logout'),
    url(r'^rec-places', views.getRecPlaces, name='rec-places'),
    url(r'^rec-photos', views.getRecPhotos, name='rec-photos'),
    url(r'^statuses', views.getStatuses, name='statuses'),
    url(r'^checkins', views.getCheckins, name='checkins'),
    url(r'^register', views.register, name='register'),
    url(r'^orders', views.getOrders, name='orders'),
    url(r'^pages/widgets$', views.widgets, name='widgets'),
    url(r'^pic-around', views.getPicAround, name='register'),
    url(r'^places-around', views.getPlacesAround, name='register'),
    url(r'^$', views.getRecPlaces, name='welcome'),
)
