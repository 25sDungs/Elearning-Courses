from courses.models import Category, Lesson, Course, Tag, Comment, User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# hiển thị địa chỉ đường dẫn image từ cloudinary
class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        d = super().to_representation(instance)
        d['image'] = instance.image.url
        return d


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        # lấy trường category_id ko lấy category để tránh phải kết các bảng
        # Không sử dụng category__id
        fields = ['id', 'subject', 'image', 'created_date', 'category_id']


class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'image']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return lesson.like_set.filter(user=request.user, active=True).exists()

        return None

    class Meta:
        model = LessonSerializer.Meta.model  # Kế thừa meta.model từ lớp cha
        fields = LessonSerializer.Meta.fields + ['content', 'tags', 'liked']  # Thêm 2 trường thuộc tính từ lớp cha


# class AuthenticatedLessonDetailsSerializer(LessonDetailSerializer):


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True  # => password chỉ có thể ghi, ko read => ko trả về trường password
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()
        return u

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

    def to_representation(self, instance):
        d = super().to_representation(instance)
        d['avatar'] = instance.avatar.url if instance.avatar else ''
        return d


class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data

    class Meta:
        model = Comment
        # updated_date không có trong bảng mà là thuộc tính update_date
        fields = ['id', 'content', 'created_date', 'update_date', 'user', 'lesson']
        extra_kwargs = {
            'lesson': {
                'write_only': True
            }
        }


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']
