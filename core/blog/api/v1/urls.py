from rest_framework import routers
from . import views

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("post", views.PostViewSet, basename="post")

urlpatterns = []
urlpatterns += router.urls
