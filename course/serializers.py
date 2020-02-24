# from rest_framework import serializers
#
# from account.models import Account
# from course.models import Course, CourseSubToSubCategory, CourseCategory
#
#
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['course_title', 'course_slug', 'course_content', 'course_media', 'course_created_date',
#                   'course_author', 'course_view']
#
#
# class CourseCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseCategory
#         fields = ['course_category_title', 'course_category_slug', 'course_category_description', 'course_category_created_date', 'course_category_creator']
#
#
# class CourseSubToSubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseSubToSubCategory
#         fields = ['course_sub_to_sub_category_title', 'course_sub_to_sub_category_slug',
#                   'course_sub_to_sub_category_created_date', 'course_sub_to_sub_category_description',
#                   'course_sub_to_sub_category_creator']
