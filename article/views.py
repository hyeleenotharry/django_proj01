from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Article, Comment
from .serializers import (
    ArticleCreateSerializer,
    ArticleListSerializer,
    ArticleSerializer,
    CommentSerializer,
    CommentUserSerializer,
)
from rest_framework.generics import get_object_or_404


# Create your views here.
class ArticleCreate(APIView):
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleList(APIView):
    def get(self, request, user_id):
        articles = Article.objects.filter(author_id=user_id)

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetail(APIView):
    def get(self, request, user_id, article_id):
        article = Article.objects.get(id=article_id)
        if article.author == request.user:
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.author == request.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.author == request.user:
            article.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class CommentCreate(APIView):
    def post(self, request, article_id):
        serializer = CommentUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get(self, request, article_id, comment_id):
        articles = get_object_or_404(Article, id=article_id)
        comments = articles.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author == request.user:
            serializer = CommentUserSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=article_id)
        if comment.author == request.user:
            comment.delete()
            return Response("삭제 완료", status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def post(self, request, article_id):
        permission_classes = [permissions.IsAuthenticated]
        article = get_object_or_404(Article, id=article_id)
        if article in request.user.like_articles.all():
            article.likes.remove(request.user)
            return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요를 눌렀습니다.", status=status.HTTP_200_OK)
