from django.urls import path, include
from rest_framework.routers import DefaultRouter

from playlist_connect_api import views

router = DefaultRouter()
router.register("playlist-pairs", views.PlaylistPairsViewSet)

urlpatterns = [path("", include(router.urls))]
