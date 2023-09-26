from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from article.models import Article, Comment
from .models import User
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from .serializers import UserSerializer, UserProfileSerializer, UserListSerializer
from article.serializers import (
    ArticleListSerializer,
    CommentUserSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class SignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # serializer 을 저장하기 전에 데이터에 접근하려면 data 가 아니라 validated_data 를 써야함
            serializer.save()
            return Response("회원가입 완료", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]

        return Response(f"{request.data} 로그아웃", status=status.HTTP_200_OK)


class Cancel(APIView):
    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]
        user = get_object_or_404(User, id=request.user.id)
        if user:
            user.delete()

            return Response("탈퇴했습니다.", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("없는 사용자입니다.", status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class MyArticle(APIView):
    def get(self, request, user_id):
        articles = Article.objects.filter(author_id=user_id)

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class MyComment(APIView):
    def get(self, request, user_id):
        comments = Comment.objects.filter(author_id=user_id)

        serializer = CommentUserSerializer(comments, many=True)
        return Response(serializer.data)


class FollowView(APIView):
    def post(self, request, user_id):
        permission_classes = [permissions.IsAuthenticated]
        you = get_object_or_404(User, id=user_id)
        if you in request.user.follower.all():
            you.followee.remove(request.user)
            return Response("팔로우 취소했습니다.", status=status.HTTP_200_OK)
        else:
            you.followee.add(request.user)
            return Response("팔로우 했습니다.", status=status.HTTP_200_OK)
