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
        url(r'^run-script-pred/', views.run_script_pred),
        url(r'^run-script-erp/', views.run_script_erp),
        url(r'^run-script-comp/', views.run_script_comp)
]