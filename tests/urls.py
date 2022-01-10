from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('empty/', TemplateView.as_view(template_name='empty.html'), name='empty'),
    path('admin/', admin.site.urls),
]
