from django.shortcuts import render


def all_schools(request):
    return render(request, "ankades/school/schools.html")