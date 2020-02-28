from django.shortcuts import render


def all_departments(request):
    return render(request, "ankades/department/departments.html")