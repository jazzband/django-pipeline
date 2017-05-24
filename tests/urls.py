from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^empty/$', TemplateView.as_view(template_name="empty.html"), name="empty"),
    url(r'^admin/', admin.site.urls),
]
