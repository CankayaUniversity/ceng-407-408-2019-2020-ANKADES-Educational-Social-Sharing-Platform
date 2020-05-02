import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from ankadescankaya.views import current_user_group
from exam.models import School, Department, Lecture


def admin_all_lectures(request, departmentCode):
    """
    :param request:
    :param departmentCode:
    :return:
    """
    try:
        lectures = Lecture.objects.filter(departmentId__departmentCode=departmentCode, isActive=True)
    except:
        messages.error(request, "Ders bulunamadı.")
        return redirect("admin_all_schools")
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "lectures": lectures,
    }
    return render(request, "adminpanel/exam/all-lectures.html", context)


def admin_add_lecture(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        schools = School.objects.filter(isActive=True).order_by('slug')
        departments = Department.objects.filter(isActive=True).order_by('slug')
        getSchool = request.GET.get("school")
        context = {
            "userGroup": userGroup,
            "schools": schools,
            "departments": departments,
        }
        if getSchool:
            instance = School.objects.get(slug=getSchool)
            departments = Department.objects.filter(schoolId__slug=getSchool, isActive=True)
            addContext = {
                "userGroup": userGroup,
                "getSchool": getSchool,
                "instance": instance,
                "departments": departments,
            }
            return render(request, "adminpanel/exam/add/add-lecture.html", addContext)
        if request.method == "POST":
            instance = Lecture()
            departmentId = request.POST["department"]
            title = request.POST.get("title")
            lectureCode = request.POST.get("lectureCode")
            check = Lecture.objects.filter(departmentId__id=departmentId, title=title, lectureCode=lectureCode)
            if check:
                messages.error(request, "Bu bölüme daha önce " + str(title) + " dersi tanımlanmış.")
                return redirect("admin_add_lecture")
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
                return redirect("admin_add_lecture")
        return render(request, "adminpanel/exam/add/add-lecture.html", context)
    else:
        return redirect("index")