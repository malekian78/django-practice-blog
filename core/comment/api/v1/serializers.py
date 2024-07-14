from rest_framework import serializers
from comment.models import Comment
from blog.models import Post
from accounts.models import Profile


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    status = serializers.ReadOnlyField()
    author = serializers.SlugRelatedField(read_only=True, slug_field="user__email")
    
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "content",
            "status",
            "created_date",
        )
    read_only_fields = ["author", "status"]
    
    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user=self.context.get("request").user.id
        )
        return super().create(validated_data)

