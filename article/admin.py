# from .forms import AnonymousForm
from django.contrib import admin
from article.models import Article, Comment, Category, Anonymous
from django import forms

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)


class AnonymousForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Anonymous
        fields = "__all__"


admin.site.register(Anonymous)
