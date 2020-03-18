from django.shortcuts import render


def all_departments(request):
    return render(request, "ankades/../../templates/test/department/departments.html")