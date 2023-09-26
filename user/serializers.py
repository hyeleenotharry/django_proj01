from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from article.serializers import ArticleListSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(many=True)
    followee = serializers.StringRelatedField(many=True)
    article_set = ArticleListSerializer(many=True)
    like_articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "follower",
            "followee",
            "article_set",
            "like_articles",
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "password",
            "email",
            "username",
            "fullname",
            "nickname",
            "birthday",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        # set password 로 해싱을 해줘야함
        user.set_password(password)

        user.save()

        return user

    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        # set password 로 해싱을 해줘야함
        user.set_password(password)
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        # ...

        return token
