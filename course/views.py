from rest_framework import viewsets

from course.models import Course, CourseSubToSubCategory, CourseCategory
from course.serializers import CourseSerializer, CourseSubToSubCategorySerializer, CourseCategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-course_created_date')
    serializer_class = CourseSerializer

class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseSubToSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseSubToSubCategory.objects.all().order_by('-course_sub_to_sub_category_created_date')
    serializer_class = CourseSubToSubCategorySerializer
