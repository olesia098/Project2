from datetime import timedelta


from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsPostAuthor
from .serializers import RatingSerializers, LikeSerializers, ImageSerializers
from rest_framework import generics, viewsets, status
from main.models import *
from main.serializers import PostSerializers, CategorySerializers

User = get_user_model()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny, ]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated, ]

        return [permission()for permission in permissions]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     weeks_count = int(self.request.query_params.get('week', 0))
    #     if weeks_count > 0:
    #         start_date = timezone.now() - timedelta(weeks=weeks_count)
    #         queryset = queryset.filter(created_at__gte=start_date)
    #     return queryset

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = PostSerializers(queryset, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(item_name__icontains=q) | Q(text__icontains=q))
        serializers = PostSerializers(queryset, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['Post'], detail=True)
    def rating(self, request, pk):  # http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(product=self.get_object(), author=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(author=request.user, product=self.get_object(), rating=request.data['rating'])
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = ImageSerializers

    def get_serializer_context(self):
        return {'request': self.request}




