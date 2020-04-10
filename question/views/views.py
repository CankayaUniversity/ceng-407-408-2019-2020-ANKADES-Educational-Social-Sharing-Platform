import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView

from account.models import AccountLogs
from account.views.views import current_user_group
from question.forms import QuestionForm, EditQuestionForm
from question.models import Question, QuestionComment, QuestionCategory


def add_question(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    form = QuestionForm(request.POST or None)
    activity = AccountLogs()
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
        instance = Question.objects.get(questionNumber=questionNumber, slug=slug)
        instance.view += 1
        questionAnswers = QuestionComment.objects.filter(questionId__slug=slug, questionId__questionNumber=questionNumber, isRoot=True, isReply=False)
        answerReply = QuestionComment.objects.filter(isReply=True, isRoot=False)
        try:
            certifiedAnswer = QuestionComment.objects.get(questionId__slug=slug, questionId__questionNumber=questionNumber, isCertified=True)
        except:
            certifiedAnswer = None
    except:
        return render(request, "404.html")
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "instance": instance,
        "questionAnswers": questionAnswers,
        "certifiedAnswer": certifiedAnswer,
        "answerReply": answerReply,
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


def add_question_answer(request, slug, questionNumber):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AccountLogs()
    activity.application = "Question"
    activity.creator = currentUser
    activity.title = "Soru Yorum Ekleme"
    activity.method = "POST"
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    try:
        instance = Question.objects.get(slug=slug, questionNumber=questionNumber)
        if request.method == "POST":
            content = request.POST.get("content")
            new_answer = QuestionComment(content=content, creator=request.user)
            new_answer.questionId = instance
            new_answer.isActive = True
            new_answer.isRoot = True
            new_answer.answerNumber = get_random_string(length=32)
            new_answer.save()
            new_answer.parentId_id = new_answer.id
            new_answer.save()
            activity.description = "Soruya yeni bir cevap eklendi. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + " ."
            activity.save()
            messages.success(request, "Cevabınız başarıyla oluşturuldu.")
        return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}), context)
    except:
        messages.error(request, "Cevap vermek istediğiniz soru bulunamadı.")
        return redirect("all_questions")


def add_question_answer_reply(request, slug, questionNumber, answerNumber):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AccountLogs()
    activity.application = "Question"
    activity.creator = currentUser
    activity.title = "Soru Yorum Ekleme"
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    try:
        instance = Question.objects.get(slug=slug, questionNumber=questionNumber)
        parentAnswer = QuestionComment.objects.get(answerNumber=answerNumber)
        if request.method == "POST":
            content = request.POST.get("content")
            new_answer = QuestionComment(content=content, creator=request.user)
            new_answer.questionId = instance
            new_answer.answerNumber = get_random_string(length=32)
            new_answer.parentId.answerNumber = parentAnswer.answerNumber
            new_answer.isActive = True
            new_answer.isRoot = False
            new_answer.save()
            new_answer.parentId_id = new_answer.id
            activity.description = "Soruya yeni bir cevap eklendi. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate)
            activity.save()
            messages.success(request, "Cevabınız başarıyla oluşturuldu.")
        return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}), context)
    except:
        messages.error(request, "Cevap vermek istediğiniz soru bulunamadı.")
        return redirect("all_questions")


def delete_question(request, questionNumber):
    return None


class QuestionLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        questionNumber = self.kwargs.get("questionNumber")
        obj = get_object_or_404(Question, slug=slug, questionNumber=questionNumber)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        obj.view -= 1
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