from .models import Article, Comment, Anonymous
from rest_framework import serializers


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content", "image")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("article",)  # 1개라도 , 써줘야 함


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class AnonymousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anonymous
        exclude = ("article",)  # 1개라도 , 써줘야 함


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comment_set.count() + obj.anonymous_set.count()

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "content",
            "author",
            "image",
            "updated_at",
            "likes_count",
            "comment_count",
        )


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    anonymous_set = AnonymousSerializer(many=True)
    likes = serializers.StringRelatedField(
        many=True
    )  # likes 와 연관된 User 모델의 __str__ 타입이 이메일이므로 이메일 형태로 나타남

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Article
        fields = "__all__"
