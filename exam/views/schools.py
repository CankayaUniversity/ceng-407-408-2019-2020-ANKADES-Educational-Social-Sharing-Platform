from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from exam.models import School, Department, Lecture, Exam, ExamTag


def all_schools(request):
    schools = School.objects.all()
    departments = Department.objects.all()
    lectures = Lecture.objects.all()
    exams = Exam.objects.all()
    examTags = ExamTag.objects.all()
    context = {
        "schools": schools,
        "departments": departments,
        "lectures": lectures,
        "exams": exams,
        "examTags": examTags,
    }
    return render(request, "ankades/exam/all-schools.html", context)
