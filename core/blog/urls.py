from django.urls import include, path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/create/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/edit/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/delete/<int:pk>/", views.PostDeleteView.as_view(), name="post-delete"),
]
