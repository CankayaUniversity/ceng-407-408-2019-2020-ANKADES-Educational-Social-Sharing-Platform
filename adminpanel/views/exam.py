import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountGroup
from adminpanel.forms import AdminSchoolForm, AdminDepartmentForm, AdminTermForm, AdminLectureForm, AdminExamForm
from exam.models import School, Department, Term, Lecture, Exam


# School
@login_required(login_url="login_admin")
def admin_schools(request):
    """
    :param request:
    :return:
    """
    schools = School.objects.all()
    context = {
        "schools": schools,
    }
    return render(request, "admin/exam/school/all-schools.html", context)


@login_required(login_url="login_admin")
def admin_add_school(request):
    """
    :param request:
    :return:
    """
    form = AdminSchoolForm(request.POST or None)
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
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        instance = get_object_or_404(School, slug=slug)
        form = AdminSchoolForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Okul başarıyla düzenlendi !")
            return redirect("admin_schools")
        return render(request, "admin/exam/school/edit-school.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_school(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(School, slug=slug)
    instance.delete()
    messages.success(request, "Okul başarıyla silindi !")
    return redirect("admin_schools")


# Department
@login_required(login_url="login_admin")
def admin_departments(request):
    """
    :param request:
    :return:
    """
    departments = Department.objects.all()
    context = {
        "departments": departments,
    }
    return render(request, "admin/exam/department/all-departments.html", context)


@login_required(login_url="login_admin")
def admin_add_department(request):
    """
    :param request:
    :return:
    """
    form = AdminDepartmentForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Bölüm başarıyla eklendi !")
        return redirect("admin_departments")
    return render(request, "admin/exam/department/add-department.html", context)


@login_required(login_url="login_admin")
def admin_edit_department(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        instance = get_object_or_404(Department, slug=slug)
        form = AdminDepartmentForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Bölüm başarıyla düzenlendi !")
            return redirect("admin_departments")
        return render(request, "admin/exam/school/edit-department.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_department(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Department, slug=slug)
    instance.delete()
    messages.success(request, "Bölüm başarıyla silindi !")
    return redirect("admin_schools")


# Term
@login_required(login_url="login_admin")
def admin_terms(request):
    """
    :param request:
    :return:
    """
    terms = Term.objects.all()
    context = {
        "terms": terms,
    }
    return render(request, "admin/exam/term/all-terms.html", context)


@login_required(login_url="login_admin")
def admin_add_term(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AdminTermForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form
            messages.success(request, "Dönem başarıyla eklendi !")
            return redirect("admin_terms")
    else:
        form = AdminTermForm(request.POST)
    return render(request, "admin/exam/term/add-term.html", {"form": form})


@login_required(login_url="login_admin")
def admin_edit_term(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
        instance = get_object_or_404(Term, slug=slug)
        form = AdminTermForm(request.POST or None, request.FILES or None, instance=instance)
        context = {
            "form": form,
            "adminGroup": adminGroup
        }
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Dönem başarıyla düzenlendi !")
            return redirect("admin_terms")
        return render(request, "admin/exam/term/edit-term.html", context)
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_term(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Term, slug=slug)
    instance.delete()
    messages.success(request, "Dönem başarıyla silindi !")
    return redirect("admin_terms")


# Lecture
@login_required(login_url="login_admin")
def admin_lectures(request):
    """
    :param request:
    :return:
    """
    lectures = Lecture.objects.all()
    context = {
        "lectures": lectures,
    }
    return render(request, "admin/exam/lecture/all-lectures.html", context)


@login_required(login_url="login_admin")
def admin_add_lecture(request):
    """
    :param request:
    :return:
    """
    form = AdminLectureForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Dönem başarıyla eklendi !")
        return redirect("admin_schools")
    return render(request, "admin/exam/lecture/add-lecture.html", context)


@login_required(login_url="login_admin")
def admin_edit_lecture(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Lecture, slug=slug)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        form = AdminLectureForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            messages.success(request, "Ders başarıyla düzenlendi !")
            return redirect("admin_lectures")
    return render(request, "admin/exam/lecture/edit-lecture.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_lecture(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    instance = get_object_or_404(Lecture, slug=slug)
    if adminGroup:
        instance.delete()
        messages.success(request, "Ders başarıyla silindi !")
        return redirect("admin_lectures")
    else:
        instance.isActive = False
        messages.warning(request, "Ders başarıyla etkisizleştirildi !")
        return redirect("admin_lectures")


# Exam
@login_required(login_url="login_admin")
def admin_exams(request):
    """
    :param request:
    :return:
    """
    exams = Exam.objects.all()
    context = {
        "exams": exams,
    }
    return render(request, "admin/exam/pre-exam/all-exams.html", context)


@login_required(login_url="login_admin")
def admin_add_exam(request):
    """
    :param request:
    :return:
    """
    form = AdminExamForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Sınav arşivi başarıyla eklendi !")
        return redirect("admin_exams")
    return render(request, "admin/exam/pre-exam/add-exam.html", context)


@login_required(login_url="login_admin")
def admin_edit_exam(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        instance = get_object_or_404(Exam, slug=slug)
        form = AdminExamForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Sınav arşivi başarıyla düzenlendi !")
            return redirect("admin_exams")
        return render(request, "admin/exam/pre-exam/edit-exam.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_exam(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    instance = get_object_or_404(Lecture, slug=slug)
    if adminGroup:
        instance.delete()
        messages.success(request, "Ders başarıyla silindi !")
        return redirect("admin_lectures")
    else:
        instance.isActive = False
        messages.warning(request, "Sınav başarıyla etkisizleştirildi !")
        return redirect("admin_lectures")