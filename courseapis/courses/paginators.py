from rest_framework import pagination


class CoursePagination(pagination.PageNumberPagination):
    page_size = 6


class CommentPagination(pagination.PageNumberPagination):
    page_size = 3
