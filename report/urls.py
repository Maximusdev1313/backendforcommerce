from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register('report', ReportViewSet)

urlpatterns = [
    path('', include(router.urls) ),
    
]