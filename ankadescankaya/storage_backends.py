from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION


class ArticleMediaStorage(S3Boto3Storage):
    location = settings.AWS_ARTICLE_MEDIA_LOCATION
    file_overwrite = False


class ExamMediaStorage(S3Boto3Storage):
    location = settings.AWS_EXAM_MEDIA_LOCATION
    file_overwrite = False


class SchoolMediaStorage(S3Boto3Storage):
    location = settings.AWS_SCHOOL_MEDIA_LOCATION
    file_overwrite = False


class CourseMediaStorage(S3Boto3Storage):
    location = settings.AWS_COURSE_MEDIA_LOCATION
    file_overwrite = False


class UserMediaStorage(S3Boto3Storage):
    location = settings.AWS_USER_MEDIA_LOCATION
    file_overwrite = False


class SupportMediaStorage(S3Boto3Storage):
    location = settings.AWS_SUPPORT_MEDIA_LOCATION
    file_overwrite = False
