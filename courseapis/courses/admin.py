from django.contrib import admin
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from courses.models import Category, Course, Lesson, Tag


class LessonFrom(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


# Register your models here.
class MyLesson(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'course']
    list_filter = ['subject']
    readonly_fields = ['image_view']
    form = LessonFrom

    def image_view(self, lesson):
        return mark_safe(f'<img src="/static/{lesson.image.name}" width="120" />')

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
        js = ('/static/js/script.js',)


class MyCourse(admin.ModelAdmin):
    list_display = ['subject', 'image_view', 'created_date']
    readonly_fields = ['image_view']

    def image_view(self, courses):
        return mark_safe(f'<img src="/static/{courses.image.name}" width="120" />')


admin.site.register(Category)
admin.site.register(Course, MyCourse)
admin.site.register(Lesson, MyLesson)
admin.site.register(Tag)
