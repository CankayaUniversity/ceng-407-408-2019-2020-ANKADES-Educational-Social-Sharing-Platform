from django.shortcuts import render

# Create your views here.
from account.views.views import current_user_group
from question.forms import AddQuestionForm
from question.models import Question


def add_question(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    form = AddQuestionForm(request.POST or None)
    if request.POST == "POST":
        categoryId = request.POST['categoryId']
        title = request.POST.get('title')
        if form.is_valid():
            description = form.cleaned_data.get('description')
        instance = Question(categoryId=categoryId, title=title)
        instance.isActive
        instance.save()
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "ankades/question/add-question.html", context)


def index(request):
    return None