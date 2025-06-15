
# ================= restaurant/urls.py =================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet

router = DefaultRouter()
router.register(r'items', MenuItemViewSet, basename='menuitem')

urlpatterns = [
    path('', include(router.urls)),
]
