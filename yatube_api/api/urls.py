from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    PostViewSet, GroupViewSet,
    CommentViewSet, FollowViewSet
)


router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)


comment_router = SimpleRouter()
comment_router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include([
        path('auth/', include('djoser.urls')),
        path('', include('djoser.urls.jwt')),
        path('', include(router.urls)),
        path('posts/<int:post_id>/', include(comment_router.urls)),
    ])),
]
