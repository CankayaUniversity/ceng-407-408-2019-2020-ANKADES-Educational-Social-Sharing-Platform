from django.shortcuts import render

# Create your views here.

def all_schools(request):
    return render(request, "ankades/school/schools.html")

def all_departments(request):
    return render(request, "ankades/department/departments.html")

