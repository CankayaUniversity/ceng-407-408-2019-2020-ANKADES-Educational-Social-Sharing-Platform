from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from account.models import Account
from article.models import Article
from course.models import Course
from exam.models import School, Exam, Lecture, Department
from question.models import Question


class SearchKeyword(DetailView):
    @staticmethod
    def search_article(request):
        """
        :param request:
        :return:
        """
        article = None
        keyword = request.GET.get("keyword")
        if keyword:
            article = Article.objects.filter(
                Q(title__icontains=keyword, isActive=True) | Q(description__icontains=keyword, isActive=True) | Q(
                    postNumber__icontains=keyword, isActive=True))
        return article

    @staticmethod
    def search_question(request):
        """
        :param request:
        :return:
        """
        question = None
        keyword = request.GET.get("keyword")
        if keyword:
            question = Question.objects.filter(
                Q(title__icontains=keyword, isActive=True) | Q(description__icontains=keyword, isActive=True) | Q(
                    postNumber__icontains=keyword, isActive=True))
        return question

    @staticmethod
    def search_course(request):
        """
        :param request:
        :return:
        """
        course = None
        keyword = request.GET.get("keyword")
        # course_category = Categories.all_categories()[6].values("title")
        if keyword:
            course = Course.objects.filter(
                Q(title__icontains=keyword, isActive=True) | Q(description__icontains=keyword, isActive=True) | Q(
                    courseNumber__icontains=keyword, isActive=True) | Q(introduction__icontains=keyword, isActive=True))
        return course

    @staticmethod
    def search_school(request):
        """
        :param request:
        :return:
        """
        school = None
        keyword = request.GET.get("keyword")
        if keyword:
            school = School.objects.filter(Q(title__icontains=keyword, isActive=True) | Q(slug__icontains=keyword, isActive=True))
        return school

    @staticmethod
    def search_lecture(request):
        """
        :param request:
        :return:
        """
        lecture = None
        keyword = request.GET.get("keyword")
        if keyword:
            lecture = Lecture.objects.filter(
                Q(title__icontains=keyword, isActive=True) | Q(lectureCode__icontains=keyword, isActive=True))
        return lecture

    @staticmethod
    def search_exam(request):
        """
        :param request:
        :return:
        """
        exam = None
        keyword = request.GET.get("keyword")
        if keyword:
            exam = Exam.objects.filter(Q(title__icontains=keyword, isActive=True))
        return exam

    @staticmethod
    def search_account(request):
        """
        :param request:
        :return:
        """
        account = None
        keyword = request.GET.get("keyword")
        if keyword:
            account = Account.objects.filter(
                Q(email__icontains=keyword, is_active=True) | Q(username__icontains=keyword, is_active=True) |
                Q(first_name__icontains=keyword, is_active=True) | Q(last_name__icontains=keyword, is_active=True))
        return account
