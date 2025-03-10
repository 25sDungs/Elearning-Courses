from courses.models import Category, Lesson, Course, Tag, Comment, User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# hiển thị địa chỉ đường dẫn image từ clouad
class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        d = super().to_representation(instance)
        d['image'] = instance.image.url
        return d


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'category_id', 'image']


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

    class Meta:
        model = LessonSerializer.Meta.model  # Kế thừa meta từ lớp cha
        fields = LessonSerializer.Meta.fields + ['content', 'tags']  # Thêm 2 trường thuộc tính từ lớp cha


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()
        return u

    def to_representation(self, instance):
        d = super().to_representation(instance)
        d['avatar'] = instance.image.url
        return d


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # update_date not updated_date
        fields = ['id', 'content', 'created_date', 'update_date', 'user']
