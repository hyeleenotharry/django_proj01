from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ArticleCreate.as_view(), name="article"),
    path("<int:user_id>/", views.ArticleList.as_view(), name="article-list"),
    path(
        "<int:user_id>/<int:article_id>/",
        views.ArticleDetail.as_view(),
        name="article-detail",
    ),
    path("<int:article_id>/comment/", views.CommentCreate.as_view(), name="comment"),
    path(
        "<int:article_id>/comment/<int:comment_id>/",
        views.CommentDetail.as_view(),
        name="comment-detail",
    ),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like-view"),
]

# - 게시글 작성
#     - 테이블 구성에 맞게 게시글 정보를 입력받아 게시글을 작성합니다.
#     - 로그인 한 사용자가 아니라면 게시글을 작성할 수 없습니다.
# - 게시글 목록 조회
#     - 사용자의 고유값을 사용해 특정 사용자가 작성한 게시글 목록을 조회합니다.
#     - ex) localhost:8000/article/sparta/
#         - sparta에는 사용자의 id, username, nickname과 같은 고유값을 지정합니다.
# - 특정 게시글 조회
#     - 사용자의 고유값 및 게시글의 고유값을 사용해 게시글을 조회합니다.
#     - 특정 게시글을 조회할 때 해당 게시글에 작성된 댓글들도 같이 조회합니다.
#     - ex) localhost:8000/article/sparta/1/
# - 게시글 수정
#     - 게시글의 제목 혹은 내용을 수정합니다. 본인이 작성한 게시글 외에는 수정 할 수 없습니다.
# - 게시글 삭제
#     - 게시글을 삭제합니다. 본인이 작성한 게시글 외에는 삭제할 수 없습니다.

# - 댓글 작성
#     - 테이블 구성에 맞게 댓글 정보를 입력받아 댓글을 작성합니다.
#     - 로그인 한 사용자가 아니라면 댓글을 작성할 수 없습니다.
# - 댓글 수정
#     - 댓글 내용을 수정합니다. 본인이 작성한 댓글 외에는 수정 할 수 없습니다.
# - 댓글 삭제
#     - 댓글을 삭제합니다. 본인이 작성한 댓글 외에는 삭제할 수 없습니다.
