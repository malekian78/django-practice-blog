from rest_framework import serializers
from datetime import datetime

from blog.models import Post, Category
from accounts.models.profile import Profile
from comment.api.v1.serializers import CommentSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    status = serializers.ReadOnlyField()
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field="user__email")
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "slug",
            "status",
            "image",
            "category",
            "body",
            "snippet",
            "comments",  # Include comments field
            "relative_url",
            "absolute_url",
            "updated_date",
            "created_date",
        )
    
    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            obj.pk
        )
    
    # نمایش کامنت هایی که فقط تایید شدند
    def get_comments(self, obj):
        # Filter comments to include only those with status=True
        comments = obj.comment.filter(status=True)
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print(request.__dict__)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("body", None)
        
        # category نمایش
        # باشد many=True, هست باید ManyToMany دقت کنید چون رابطه 
        rep['category'] = CategorySerializer(instance.category.all(), many=True, context={'request': request}).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user=self.context.get("request").user.id
        )
        return super().create(validated_data)



