import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

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
        getDepartment = request.GET.get("department")
        if getSchool:
            selectedSchool = School.objects.get(slug=getSchool)
            departments = Department.objects.filter(schoolId__slug=getSchool, isActive=True)
            context = {
                "userGroup": userGroup,
                "getSchool": getSchool,
                "selectedSchool": selectedSchool,
                "departments": departments,
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
            return render(request, "ankades/exam/add/exam/select-school.html", context)
        if getDepartment:
            department = Department.objects.get(slug=getDepartment)
            lectures = Lecture.objects.filter(departmentId=department)
            terms = Term.objects.all()
            context = {
                "userGroup": userGroup,
                "getSchool": getSchool,
                "lectures": lectures,
                "terms": terms,
                "department": department,
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
            if request.method == 'POST':
                new_exam = Exam()
                title = request.POST.get('title')
                term = request.POST.get('term')
                owner = request.POST.get('owner')
                lectureCode = request.POST['lectureCode']
                if request.FILES:
                    media = request.FILES.get('media')
                    fs = FileSystemStorage()
                    fs.save(media.name, media)
                    new_exam.media = media
                new_exam.title = title
                new_exam.isActive = False
                new_exam.createdDate = datetime.datetime.now()
                new_exam.examDate = datetime.datetime.now()
                new_exam.creator = request.user
                new_exam.owner = owner
                new_exam.examNumber = get_random_string(length=32)
                new_exam.lectureId_id = lectureCode
                new_exam.termId_id = term
                new_exam.save()
                messages.success(request, "Başarıyla sınav eklendi.")
                return redirect("all_schools")
            return render(request, "ankades/exam/add/add-exam.html", context)
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
            return render(request, "ankades/exam/add/exam/select-school.html", context)
    else:
        return redirect("index")


def lecture_exam(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    exams = Exam.objects.filter(lectureId__slug=slug, isActive=True)
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
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
    return render(request, "ankades/exam/lecture-exam.html", context)