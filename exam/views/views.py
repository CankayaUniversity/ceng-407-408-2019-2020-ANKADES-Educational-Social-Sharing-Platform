import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.views.views import current_user_permission
from ankadescankaya.views import current_user_group, Categories
from exam.models import ExamCategory


def all_departments(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        getParent = ExamCategory.objects.get(slug=slug)
    except:
        return redirect("404")
    departments = ExamCategory.objects.filter(parentId=getParent, isActive=True, isDepartment=True)
    context = {
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
        "getParent": getParent,
        "departments": departments,
    }
    return render(request, "ankades/exam/all-departments.html", context)


@login_required(login_url="login_account")
def add_department(request):
    userPermission = current_user_permission(request, request.user)
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    schools = ExamCategory.objects.filter(isSchool=True).order_by('title')
    context = {
        "userGroup": userGroup,
        "userPermission": userPermission,
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
    if userPermission == "can_add_department" or userGroup == "admin" or userGroup == "moderator":
        if request.method == "POST":
            instance = ExamCategory()
            categoryId = request.POST["categoryId"]
            title = request.POST.get("title")
            slug = request.POST.get("slug")
            instance.title = title
            instance.slug = slug
            instance.isActive = False
            instance.creator = request.user
            instance.createdDate = datetime.datetime.now()
            instance.updatedDate = datetime.datetime.now()
            instance.isRoot = False
            instance.parentId_id = categoryId
            instance.isSchool = False
            instance.isDepartment = True
            instance.save()
            messages.success(request, "Bölüm başarıyla eklendi. Tarafımızdan incelendikten sonra aktif edilecektir.")
            return redirect("admin_add_department")
        return render(request, "ankades/exam/add-department.html", context)
    else:
        messages.error(request, "Bölüm eklemek için gerekli izne sahip değilsiniz.")
        return redirect("index")
