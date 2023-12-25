from django.urls import path
from . import views
from django.conf.urls import url
from api import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^demodata$', views.DemoApi, name='demographics_data'),
    url(r'^demodata/([0-9]+)$', views.DemoApi, name='demographics_data_int'),
    url(r'^demodata/savefile', views.SaveFileDemo, name='demographics_data_file')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)