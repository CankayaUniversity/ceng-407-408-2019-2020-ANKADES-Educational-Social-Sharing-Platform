import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from adminpanel.forms import SchoolForm, DepartmentForm
from exam.models import School, Department


#School
def admin_schools(request):
    schools = School.objects.all()
    context = {
        "schools": schools,
    }
    return render(request, "admin/exam/school/all-schools.html", context)

@login_required(login_url="login_admin")
def admin_add_school(request):
    form = SchoolForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Okul başarıyla eklendi !")
        return redirect("admin_schools")
    return render(request, "admin/exam/school/add-school.html", context)


@login_required(login_url="login_admin")
def admin_edit_school(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(School, slug=slug)
        form = SchoolForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.view += 5
            instance.save()
            messages.success(request, "Okul başarıyla düzenlendi !")
            context = {
                "form": form,
            }
            return render(request, "admin/exam/school/edit-school.html", context)
        return render(request, "admin/exam/school/edit-school.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_school(request, slug):
    instance = get_object_or_404(School, slug=slug)
    instance.delete()
    messages.success(request, "Okul başarıyla silindi !")
    return redirect("admin_schools")


#Department
def admin_departments(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
    }
    return render(request, "admin/exam/department/all-departments.html", context)


@login_required(login_url="login_admin")
def admin_add_department(request):
    form = DepartmentForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Bölüm başarıyla eklendi !")
        return redirect("admin_departmens")
    return render(request, "admin/exam/department/add-department.html", context)


@login_required(login_url="login_admin")
def admin_edit_department(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Department, slug=slug)
        form = DepartmentForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.view += 5
            instance.save()
            messages.success(request, "Bölüm başarıyla düzenlendi !")
            context = {
                "form": form,
            }
            return render(request, "admin/exam/school/edit-school.html", context)
        return render(request, "admin/exam/school/edit-department.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_department(request, slug):
    instance = get_object_or_404(Department, slug=slug)
    instance.delete()
    messages.success(request, "Bölüm başarıyla silindi !")
    return redirect("admin_schools")
