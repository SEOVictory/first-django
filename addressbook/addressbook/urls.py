from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

import contacts.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'addressbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', contacts.views.ListContactView.as_view(),
        name='contact-list'),
    url(r'^new$', contacts.views.CreateContactView.as_view(),
        name="contacts-new"),
)

urlpatterns += staticfiles_urlpatterns()
