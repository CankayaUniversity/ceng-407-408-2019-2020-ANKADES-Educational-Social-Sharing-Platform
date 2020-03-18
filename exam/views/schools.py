from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from exam.models import School, Exam


def all_schools(request):
    schools = School.objects.all()
    exams = Exam.objects.all()
    context = {
        "schools": schools,
    }
    return render(request, "ankades/../../templates/test/exam/all-schools.html", context)
