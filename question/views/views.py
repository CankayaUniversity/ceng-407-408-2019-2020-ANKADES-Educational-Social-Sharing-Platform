import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView

from ankadescankaya.views import Categories
from ankadescankaya.views import current_user_group
from question.forms import QuestionForm, EditQuestionForm
from question.models import Question, QuestionComment, QuestionCategory


def add_question(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    form = QuestionForm(request.POST or None)
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
        instance.isActive = False
        instance.description = description
        instance.questionNumber = get_random_string(length=32)
        instance.creator = request.user
        instance.createdDate = datetime.datetime.now()
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request,
                         "Soru başarıyla oluşturuldu. Moderatörlerimiz tarafından incelendikten sonra yayına alınacak.")
        return redirect("all_questions")
    context = {
        "userGroup": userGroup,
        "questionCategory": questionCategory,
        "form": form,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    return render(request, "ankades/question/add-question.html", context)


def all_questions(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    questions_categories_lists = QuestionCategory.objects.filter(isActive=True)
    questions_limit = Question.objects.filter(isActive=True).order_by('-createdDate')
    questionComment = QuestionComment.objects.filter(isActive=True)
    categories = Categories.all_categories()
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    if keyword:
        questions = Question.objects.filter(title__contains=keyword)
        context = {
            "questions": questions,
            "questions_categories_lists": questions_categories_lists,
            "questions_limit": questions_limit,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/question/all-questions.html", context)
    else:
        questions = Question.objects.filter(isActive=True)
        paginator = Paginator(questions, 12)
        try:
            question_pagination = paginator.page(page)
        except PageNotAnInteger:
            question_pagination = paginator.page(1)
        except EmptyPage:
            question_pagination = paginator.page(paginator.num_pages)
        context = {
            "questions": questions,
            "questionComment": questionComment,
            "question_pagination": question_pagination,
            "questions_categories_lists": questions_categories_lists,
            "questions_limit": questions_limit,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/question/all-questions.html", context)


def question_detail(request, slug, questionNumber):
    """
    :param request:
    :param slug:
    :param questionNumber:
    :return:
    """
    try:
        instance = Question.objects.get(questionNumber=questionNumber, slug=slug)
        userGroup = current_user_group(request, request.user)
        categories = Categories.all_categories()
        instance.view += 1
        instance.save()
        questionAnswers = QuestionComment.objects.filter(questionId__slug=slug,
                                                         questionId__questionNumber=questionNumber, isRoot=True,
                                                         isReply=False)
        answerReply = QuestionComment.objects.filter(isReply=True, isRoot=False)
        try:
            certifiedAnswer = QuestionComment.objects.get(questionId__slug=slug,
                                                          questionId__questionNumber=questionNumber, isCertified=True)
        except:
            certifiedAnswer = None
        context = {
            "userGroup": userGroup,
            "instance": instance,
            "questionAnswers": questionAnswers,
            "certifiedAnswer": certifiedAnswer,
            "answerReply": answerReply,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/question/question-detail.html", context)
    except:
        return redirect("404")


@login_required(login_url="login_account")
def confirm_answer(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        question = Question.objects.get(questionNumber=instance.questionId.questionNumber)
        if instance.questionId.creator.username == request.user.username:
            if instance.isCertified:
                instance.isCertified = False
                question.isSolved = False
                instance.save()
                question.save()
                messages.success(request, "Cevabın doğruluğunu iptal ettiniz.")
                return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                   "questionNumber": instance.questionId.questionNumber}))
            else:
                if question.isSolved:
                    messages.error(request,
                                   "Sorunun, onaylanmış cevabı bulunduğu için, işlem gerçekleştirilemedi. Lütfen önce onayı kaldırın.")
                    return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                       "questionNumber": instance.questionId.questionNumber}))
                instance.isCertified = True
                question.isSolved = True
                instance.save()
                question.save()
                messages.success(request, "Cevabın doğruluğunu onayladınız.")
                return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                   "questionNumber": instance.questionId.questionNumber}))
        else:
            return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                               "questionNumber": instance.questionId.questionNumber}))
    except:
        return redirect("404")


@login_required(login_url="login_account")
def delete_answer(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        slug = instance.questionId.slug
        questionNumber = instance.questionId.questionNumber
        if instance.questionId.creator == request.user or instance.creator == request.user:
            instance.delete()
            messages.success(request, "Cevap başarıyla silindi.")
            return redirect(reverse("question_detail", kwargs={"slug": slug, "questionNumber": questionNumber}))
        else:
            return redirect("all_questions")
    except:
        return redirect("404")


@login_required(login_url="login_account")
def edit_question(request, slug, questionNumber):
    """
    :param request:
    :param slug:
    :param questionNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        instance = Question.objects.get(questionNumber=questionNumber, slug=slug)
        form = EditQuestionForm(request.POST or None, instance=instance)
        if instance.creator == request.user:
            if request.method == "POST":
                instance = form.save(commit=False)
                value = request.POST['value']
                title = request.POST.get('title')
                if form.is_valid():
                    description = form.cleaned_data.get("description")
                instance.categoryId_id = value
                instance.title = title
                instance.description = description
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Sorunuz başarıyla güncellendi")
                return redirect(reverse("question_detail",
                                        kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}))
        else:
            messages.error(request, "Bu soru size ait değil !")
            return redirect("index")
        context = {
            "userGroup": userGroup,
            "instance": instance,
            "form": form,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/question/edit-question.html", context)
    except:
        return render(request, "404.html")


@login_required(login_url="login_account")
def add_question_answer(request, slug, questionNumber):
    """
    :param request:
    :param slug:
    :param questionNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
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
            messages.success(request, "Cevabınız başarıyla oluşturuldu.")
        return redirect(
            reverse("question_detail", kwargs={"slug": instance.slug, "questionNumber": instance.questionNumber}),
            context)
    except:
        return redirect("404")


@login_required(login_url="login_account")
def add_question_answer_reply(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        if request.method == "POST":
            reply = request.POST.get("reply")
            new_answer = QuestionComment(content=reply, creator=request.user)
            new_answer.questionId = instance.questionId
            new_answer.answerNumber = get_random_string(length=32)
            new_answer.parentId_id = instance.id
            new_answer.isActive = True
            new_answer.isRoot = False
            new_answer.isReply = True
            new_answer.save()
            messages.success(request, "Cevabınız başarıyla oluşturuldu.")
        return redirect(
            reverse("question_detail", kwargs={"slug": instance.questionId.slug, "questionNumber": instance.questionId.questionNumber}),
            context)
    except:
        messages.error(request, "Cevap vermek istediğiniz soru bulunamadı.")
        return redirect("all_questions")


@login_required(login_url="login_account")
def delete_question(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    try:
        instance = Question.objects.get(slug=slug)
        if instance.isActive:
            instance.isActive = False
            instance.save()
        return redirect("all_questions")
    except:
        return redirect("404")


def question_category_page(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        questionCategory = QuestionCategory.objects.get(slug=slug)
        questions = Question.objects.filter(categoryId=questionCategory)
        context = {
            "questionCategory": questionCategory,
            "questions": questions,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/question/get-question-category.html", context)
    except:
        return redirect("404")


@login_required(login_url="login_account")
def question_vote_comment(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        user = request.user
        if user in instance.votes.all():
            instance.votes.remove(user)
            messages.success(request, "Verdiğiniz oy başarıyla silindi.")
            return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                               "questionNumber": instance.questionId.questionNumber}))
        else:
            instance.votes.add(user)
            messages.success(request, "Cevap oylamanız başarıyla gerçekleştirildi")
            return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                               "questionNumber": instance.questionId.questionNumber}))
    except:
        messages.error(request, "Cevap bulunamadı.")
        return redirect("all_questions")


class QuestionAnswerVoteToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        answerNumber = self.kwargs.get("answerNumber")
        obj = get_object_or_404(QuestionComment, answerNumber=answerNumber)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.votes.all():
                obj.votes.remove(user)
            else:
                obj.votes.add(user)
            messages.error(self, "Beğenildi.")
            return url_
        else:
            messages.error(self, "Giriş yapmalısınız.")
            return url_


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
