from rest_framework import viewsets

from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly
from comment.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly,]
    serializer_class = CommentSerializer
    model = Comment

    def get_queryset(self):
        return self.model.objects.filter(status=True)
