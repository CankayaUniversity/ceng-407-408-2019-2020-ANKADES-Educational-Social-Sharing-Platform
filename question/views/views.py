import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView

from account.models import AccountActivity
from account.views.views import current_user_group
from question.forms import AddQuestionForm, EditQuestionForm
from question.models import Question, QuestionComment, QuestionCategory


def add_question(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    form = AddQuestionForm(request.POST or None)
    activity = AccountActivity()
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=False))
    description = None
    if request.method == "POST":
        value = request.POST['value']
        title = request.POST.get('title')
        if form.is_valid():
            description = form.cleaned_data.get("description")
        instance = Question(isActive=True)
        instance.categoryId_id = value
        instance.title = title
        instance.description = description
        instance.questionNumber = get_random_string(length=32)
        instance.creator = currentUser
        instance.createdDate = datetime.datetime.now()
        instance.save()
        activity.createdDate = datetime.datetime.now()
        activity.creator = currentUser
        activity.method = "POST"
        activity.application = "Question"
        activity.title = "Soru Sorma"
        activity.description = str(instance.creator) + " yeni bir soru sordu. İşlemin gerçekleştirildiği tarih: " + str(
            activity.createdDate)
        activity.save()
        messages.success(request, "Soru başarıyla oluşturuldu")
        return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}))
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "questionCategory": questionCategory,
        "form": form,
    }
    return render(request, "ankades/question/add-question.html", context)


def all_questions(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "ankades/question/all-questions.html", context)


def question_detail(request, slug, questionNumber):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    try:
        getQuestion = Question.objects.get(questionNumber=questionNumber, slug=slug)
    except:
        return render(request, "404.html")
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "getQuestion": getQuestion
    }
    return render(request, "ankades/question/question-detail.html", context)


def edit_question(request, slug, questionNumber):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    try:
        instance = Question.objects.get(questionNumber=questionNumber, slug=slug)
        form = EditQuestionForm(request.POST or None, instance=instance)
        if instance.creator == currentUser:
            if request.method == "POST":
                instance = form.save(commit=False)
                value = request.POST['value']
                title = request.POST.get('title')
                if form.is_valid():
                    description = form.cleaned_data.get("description")
                instance.categoryId_id = value
                instance.title = title
                instance.description = description
                instance.save()
                messages.success(request, "Sorunuz başarıyla güncellendi")
                return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}))
        else:
            messages.error(request, "Bu soru size ait değil !")
            return redirect("index")
    except:
        return render(request, "404.html")

    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "instance": instance,
        "form": form,
    }
    return render(request, "ankades/question/edit-question.html", context)


def delete_question(request, questionNumber):
    return None


class QuestionLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        questionNumber = self.kwargs.get("questionNumber")
        obj = get_object_or_404(Question, questionNumber=questionNumber)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class QuestionLikeCommentToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        questionNumber = self.kwargs.get("questionNumber")
        obj = get_object_or_404(QuestionComment, questionId=questionNumber)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_