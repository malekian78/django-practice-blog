from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    # فکر کنم برای نمایش رسانه ها به این خط کد نیاز هست
    # parser_classes = [MultiPartParser, FormParser,]
    # REST فیلتر کردن در
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['category', 'author']

    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts

    def get_parsers(self):
        if getattr(self, "swagger_fake_view", False):
            return []
        return super().get_parsers()
