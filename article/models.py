from django.db import models
from user.models import User
from django import forms


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to="media/%Y/%m")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="like_articles", blank=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE
    )  # 역참조이므로 related_at 을 써주지 않아도 comment_set 이 디폴트로 있음
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Anonymous(models.Model):
    password = models.CharField(max_length=50)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE
    )  # 역참조이므로 related_at 을 써주지 않아도 comment_set 이 디폴트로 있음
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Anonymous Comments"
