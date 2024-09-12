from django.urls import path, include
from rest_framework.routers import DefaultRouter
from CBP.views import PostViewSet, CommentViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('comment', CommentViewSet.as_view({'post': 'create'})),
    path('category', CategoryViewSet.as_view({'get': 'list'})),
   
]