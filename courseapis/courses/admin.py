from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from courses.models import Category, Course, Lesson, Tag, Comment


class LessonFrom(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


# Register your models here.
class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'course']
    list_filter = ['subject']
    readonly_fields = ['image_view']
    form = LessonFrom

    def image_view(self, lesson):
        if lesson:
            return mark_safe(f'<img src="{lesson.image.url}" width="120" />')  # Địa chỉ ảnh Cloudinary
            # return mark_safe(f'<img src="/static/{lesson.image.name}" width="120" />')        # Địa chỉ ảnh local

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
        js = ('/static/js/script.js',)


class MyAdminSite(admin.AdminSite):
    site_header = "eCourse Online"

    def get_urls(self):
        return [path('course-stats/', self.course_stats)] + super().get_urls()

    def course_stats(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')).values('id', 'name', 'course_count')
        return TemplateResponse(request, 'admin/course-stats.html', {
            'stats': stats
        })


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['subject', 'image_view', 'created_date']
    readonly_fields = ['image_view']

    def image_view(self, courses):
        if courses:
            return mark_safe(f'<img src="{courses.image.url}" width="120" />')  # Địa chỉ ảnh Cloudinary


admin_site = MyAdminSite(name="eCourse")

admin_site.register(Category)
admin_site.register(Course, MyCourseAdmin)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(Tag)
admin_site.register(Comment)
