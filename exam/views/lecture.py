import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from ankadescankaya.views.views import current_user_group, Categories
from exam.models import Department, School, Lecture


def lectures(request, departmentCode):
    """
    :param request:
    :param departmentCode:
    :return:
    """
    try:
        lectures = Lecture.objects.filter(departmentId__departmentCode=departmentCode, isActive=True)
        allLectures = Lecture.objects.filter(isActive=True)
    except:
        messages.error(request, "Ders bulunamadı.")
        return redirect("all_schools")
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "schools": allLectures,
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
        "lectures": lectures,
    }
    return render(request, "ankades/exam/all-lectures.html", context)


def add_lecture(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        categories = Categories.all_categories()
        schools = School.objects.filter(isActive=True).order_by('slug')
        departments = Department.objects.filter(isActive=True).order_by('slug')
        getSchool = request.GET.get("school")
        context = {
            "userGroup": userGroup,
            "schools": schools,
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
        if getSchool:
            instance = School.objects.get(slug=getSchool)
            departments = Department.objects.filter(schoolId__slug=getSchool, isActive=True)
            addContext = {
                "userGroup": userGroup,
                "getSchool": getSchool,
                "instance": instance,
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
            return render(request, "ankades/exam/add/add-lecture.html", addContext)
        if request.method == "POST":
            instance = Lecture()
            departmentId = request.POST["department"]
            title = request.POST.get("title")
            lectureCode = request.POST.get("lectureCode")
            check = Lecture.objects.filter(departmentId__id=departmentId, title=title, lectureCode=lectureCode)
            if check:
                messages.error(request, "Bu bölüme daha önce " + str(title) + " dersi tanımlanmış.")
                return redirect("add_lecture")
            else:
                instance.title = title
                instance.isActive = True
                instance.creator = request.user
                instance.createdDate = datetime.datetime.now()
                instance.updatedDate = datetime.datetime.now()
                instance.departmentId_id = departmentId
                instance.lectureCode = lectureCode
                instance.save()
                messages.success(request, "Ders başarıyla eklendi.")
                # TODO should return
                return redirect("add_lecture")
        return render(request, "ankades/exam/add/add-lecture.html", context)
    else:
        return redirect("index")
