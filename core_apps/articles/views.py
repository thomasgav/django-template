import logging
from django.http import Http404
from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article, ArticleView
from .serializers import ArticleSerializer
from .filters import ArticleFilter
from .pagination import ArticlePagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "updated_at"]
    renderer_classes = [ArticlesJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"article {serializer.data.get('title')} created by {self.request.user.first_name}")


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [ArticleJSONRenderer]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(
            article=instance, user=request.user, viewer_ip=viewer_ip
        )

        return Response(serializer.data)