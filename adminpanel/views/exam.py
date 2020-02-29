import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from adminpanel.forms import SchoolForm, DepartmentForm, TermForm, LectureForm, ExamForm
from exam.models import School, Department, Term, Lecture, Exam


# School
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
            instance.save()
            messages.success(request, "Okul başarıyla düzenlendi !")
            return redirect("admin_schools")
        return render(request, "admin/exam/school/edit-school.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_school(request, slug):
    instance = get_object_or_404(School, slug=slug)
    instance.delete()
    messages.success(request, "Okul başarıyla silindi !")
    return redirect("admin_schools")


# Department
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
        return redirect("admin_departments")
    return render(request, "admin/exam/department/add-department.html", context)


@login_required(login_url="login_admin")
def admin_edit_department(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Department, slug=slug)
        form = DepartmentForm(request.POST or None, request.FILES or None, instance=instance)
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
    instance = get_object_or_404(Department, slug=slug)
    instance.delete()
    messages.success(request, "Bölüm başarıyla silindi !")
    return redirect("admin_schools")


#Term
def admin_terms(request):
    terms = Term.objects.all()
    context = {
        "terms": terms,
    }
    return render(request, "admin/exam/term/all-terms.html", context)


@login_required(login_url="login_admin")
def admin_add_term(request):
    form = TermForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Dönem başarıyla eklendi !")
        return redirect("admin_terms")
    return render(request, "admin/exam/term/add-term.html", context)


@login_required(login_url="login_admin")
def admin_edit_term(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Term, slug=slug)
        form = TermForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Dönem başarıyla düzenlendi !")
            return redirect("admin_terms")
        return render(request, "admin/exam/term/edit-term.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_term(request, slug):
    instance = get_object_or_404(Term, slug=slug)
    instance.delete()
    messages.success(request, "Dönem başarıyla silindi !")
    return redirect("admin_terms")


#Lecture
def admin_lectures(request):
    lectures = Lecture.objects.all()
    context = {
        "lectures": lectures,
    }
    return render(request, "admin/exam/lecture/all-lectures.html", context)


@login_required(login_url="login_admin")
def admin_add_lecture(request):
    form = LectureForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Ders başarıyla eklendi !")
        return redirect("admin_lectures")
    return render(request, "admin/exam/lecture/add-lecture.html", context)


@login_required(login_url="login_admin")
def admin_edit_lecture(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Lecture, slug=slug)
        form = LectureForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Ders başarıyla düzenlendi !")
            return redirect("admin_lectures")
        return render(request, "admin/exam/lecture/edit-lecture.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_lecture(request, slug):
    instance = get_object_or_404(Lecture, slug=slug)
    instance.delete()
    messages.success(request, "Ders başarıyla silindi !")
    return redirect("admin_lectures")


#Exam
def admin_exams(request):
    exams = Exam.objects.all()
    context = {
        "exams": exams,
    }
    return render(request, "admin/exam/pre-exam/all-exams.html", context)


@login_required(login_url="login_admin")
def admin_add_exam(request):
    form = ExamForm(request.POST or None)
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
    if request.user.is_authenticated:
        instance = get_object_or_404(Exam, slug=slug)
        form = ExamForm(request.POST or None, request.FILES or None, instance=instance)
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
    instance = get_object_or_404(Exam, slug=slug)
    instance.delete()
    messages.success(request, "Sınav arşivi başarıyla silindi !")
    return redirect("admin_exams")