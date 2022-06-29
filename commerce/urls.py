from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('categoriya', CategoryViewSet)
router.register('rasmlar', RasmViewSet)
router.register('productlar', ProductViewSet)
urlpatterns = [
    path('', include(router.urls) ),
    # url(r'^users/(?P<username>[a-zA-Z0-9]+)$', CategoryViewSet.as_view({'get': 'retrieve'})),
    # path('/simple/', include(router.urls) )
]