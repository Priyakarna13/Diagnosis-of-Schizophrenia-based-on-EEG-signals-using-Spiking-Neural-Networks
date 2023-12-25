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
url(r'^Pred', views.Pred),
url(r'^ERP', views.ERP),
url(r'^Comp', views.Comp)
]