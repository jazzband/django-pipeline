from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^empty/$', TemplateView.as_view(template_name="empty.html"), name="empty"),
    (r'^admin/', include(admin.site.urls)),
)
