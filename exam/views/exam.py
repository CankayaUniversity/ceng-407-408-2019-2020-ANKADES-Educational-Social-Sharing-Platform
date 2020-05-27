import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from ankadescankaya.storage_backends import ExamMediaStorage
from ankadescankaya.views.views import Categories, current_user_group
from exam.models import School, Department, Term, Lecture, Exam


def add_exam(request):
    """
    :param request:
    :return:
    """
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        schools = School.objects.filter(isActive=True).order_by('slug')
        getSchool = request.GET.get("school")
        if getSchool:
            selectedSchool = School.objects.get(slug=getSchool)
            departments = Department.objects.filter(schoolId__slug=getSchool, isActive=True)
            lectures = Lecture.objects.filter(departmentId__schoolId__slug=getSchool)
            terms = Term.objects.all()
            if request.method == 'POST':
                title = request.POST.get('title')
                term = request.POST.get('term')
                owner = request.POST.get('owner')
                getExamDate = request.POST.get('examDate')
                ownerEmail = request.POST.get('ownerEmail')
                lecture = request.POST['lecture']
                new_exam = Exam(checked=True, isActive=False)
                if request.FILES:
                    media = request.FILES.get('media')
                    fs = FileSystemStorage()
                    fs.save(media.name, media)
                    new_exam.media = media
                new_exam.title = title
                new_exam.termId_id = term
                new_exam.owner = owner
                new_exam.ownerEmail = ownerEmail
                new_exam.examDate = getExamDate
                new_exam.creator = request.user
                new_exam.examNumber = get_random_string(length=32)
                new_exam.lectureId_id = lecture
                new_exam.createdDate = datetime.datetime.now()
                new_exam.isActive = True
                new_exam.save()
                messages.success(request, "Başarıyla sınav eklendi.")
                return redirect("all_schools")
            context = {
                "userGroup": userGroup,
                "getSchool": getSchool,
                "selectedSchool": selectedSchool,
                "terms": terms,
                "lectures": lectures,
                "departments": departments,
            }
            return render(request, "ankacademy/exam/add-exam.html", context)
        else:
            context = {
                "userGroup": userGroup,
                "schools": schools,
                "articleCategories": categories[0],
                "articleSubCategories": categories[1],
                "articleLowerCategories": categories[2],
                "questionCategories": categories[3],
                "questionSubCategories": categories[4],
                "questionLowerCategories": categories[5],
                "courseCategories": categories[6],
                "courseSubCategories": categories[7],
                "courseLowerCategories": categories[8],
            }
            return render(request, "ankacademy/exam/add-exam.html", context)
    else:
        return redirect("index")


def lecture_exam(request, postNumber):
    """
    :param request:
    :param postNumber:
    :return:
    """
    try:
        instance = Lecture.objects.get(postNumber=postNumber)
    except:
        messages.error(request, "Ders bulunamadı.")
        return redirect("all_schools")
    exams = Exam.objects.filter(lectureId__postNumber=instance, isActive=True)
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "instance": instance,
        "exams": exams,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    return render(request, "ankacademy/exam/lecture-exam.html", context)