from django.conf.urls import patterns, include, url

from django.contrib import admin
from appUI import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openiPrototype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^index$', views.welcome, name='welcome'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^pages/widgets$', views.widgets, name='widgets'),
)
