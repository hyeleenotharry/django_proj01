from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", views.SignUp.as_view(), name="sign-up"),
    path("cancel/", views.Cancel.as_view(), name="cancel-account"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("<int:user_id>/", views.Profile.as_view(), name="profile"),
    path("<int:user_id>/articles/", views.MyArticle.as_view(), name="my-article"),
    path("<int:user_id>/comments/", views.MyComment.as_view(), name="my-comment"),
    path("follow/<int:user_id>/", views.FollowView.as_view(), name="following"),
]

# - 회원가입
#     - 테이블 구성에 맞게 사용자 정보를 입력받아 회원가입을 진행합니다.
# - 로그인
#     - Django의 login인 기능을 사용해 username, password를 입력받아 로그인을 진행합니다.
# - 로그아웃
#     - 로그인 한 사용자를 로그아웃 합니다.
# - 본인 정보 조회
#     - 로그인 한 사용자(본인)의 정보를 조회합니다.
# - 본인 게시글 조회
#     - 로그인 한 사용자(본인)가 작성한 게시글 목록을 조회합니다.
# - 본인 댓글 조회
#     - 로그인 한 사용자(본인)가 작성한 댓글 목록을 조회합니다.
