from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User, Comment, Like, Tag
from courses import serializers, paginators, perms
from rest_framework import viewsets, generics, parsers, status, permissions


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePagination

    # ghi đè queryset
    def get_queryset(self):
        query = self.queryset

        if self.action.__eq__('list'):
            # Thuộc tính request nằm trong self
            q = self.request.query_params.get("q")
            if q:
                query = query.filter(subject__icontains=q)

            cate_id = self.request.query_params.get("category_id")
            if cate_id:
                query = query.filter(category_id=cate_id)

        return query

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailSerializer

    def get_permissions(self):
        if self.action.__eq__('get_comments'):
            if self.request.method.__eq__('POST'):
                return [permissions.IsAuthenticated()]
        elif self.action.__eq__('like'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            t = serializers.CommentSerializer(data={
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': pk
            })
            t.is_valid(raise_exception=True)
            c = t.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)
            p = paginators.CommentPagination()
            page = p.paginate_queryset(comments, self.request)
            if page:
                serializer = serializers.CommentSerializer(page, many=True)
                return p.get_paginated_response(serializer.data)
            else:
                return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True, permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not created:
            li.active = not li.active

        li.save()
        return Response(serializers.LessonDetailSerializer(self.get_object(), context={"request": self.request}).data)

    # @action(methods=['post'], url_path='tags', detail=True)
    # def tag(self, request, pk):
    #
    #     t = serializers.TagSerializer(data={
    #         'name': request.data.get('tags'),
    #         'lesson': pk
    #     })
    #     t.is_valid(raise_exception=True)
    #     c = t.save()
    #     return Response(serializers.TagSerializer(c).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]  # Hỗ trợ JSON và FormData

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [perms.OwnerPerms()]

        return [permissions.AllowAny()]

    # get .../users/current-user/
    @action(methods=['get', 'patch'], url_path='current-user', detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        if request.method.__eq__("PATCH"):
            u = request.user

            for key in request.data:
                # Cập nhật trường dl first_name, last_name và password
                if key in ['first_name', 'last_name']:
                    setattr(u, key, request.data[key])
                elif key.__eq__('password'):
                    u.set_password(request.data[key])

            u.save()
            return Response(serializers.UserSerializer(u).data)
        else:
            return Response(serializers.UserSerializer(request.user).data)


# API Xóa cmt
class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    # Dùng queryset, không sử dụng query
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]

    # cung cấp yêu cầu bổ sung trường user và lesson
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
