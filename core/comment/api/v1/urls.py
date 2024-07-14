from rest_framework import routers
from . import views

app_name = "api-v1-comment"

router = routers.DefaultRouter()
router.register("comment", views.CommentViewSet, basename="comment")
urlpatterns = []
urlpatterns += router.urls
