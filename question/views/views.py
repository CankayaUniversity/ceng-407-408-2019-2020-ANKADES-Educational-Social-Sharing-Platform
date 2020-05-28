import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView, DetailView

from account.models import AccountFollower
from account.views.views import get_user_follower, user_articles, user_questions, user_courses, user_exams
from ankadescankaya.views.views import current_user_group, Categories
from question.forms import QuestionForm, EditQuestionForm
from question.models import Question, QuestionComment, QuestionCategory
from support.models import Report, ReportSubject


def add_question(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    form = QuestionForm(request.POST or None)
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=False))
    if request.method == "POST":
        value = request.POST.get('value')
        title = request.POST.get('title')
        if form.is_valid():
            description = form.cleaned_data.get("description")
        instance = Question(isActive=True)
        instance.categoryId_id = value
        instance.title = title
        instance.isActive = False
        instance.description = description
        instance.postNumber = get_random_string(length=32)
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
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
    }
    return render(request, "ankacademy/question/add-question.html", context)


def all_questions(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    category = request.GET.get('c')
    sub = request.GET.get('s')
    lower = request.GET.get('l')
    getLowCategory = []
    questionCat = []
    topCategories = QuestionCategoryView.getTopCategory(request)
    questionComment = QuestionComment.objects.filter(isActive=True)
    questions = Question.objects.filter(isActive=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    if category:
        top = QuestionCategory.objects.filter(catNumber=category)
        sub = QuestionCategory.objects.filter(isActive=True, parentId__catNumber=category)
        for getLower in sub:
            getLowCategory.append(getLower.catNumber)
        lower = QuestionCategory.objects.filter(isActive=True, parentId__catNumber__in=getLowCategory)
        for cat in lower:
            questionCat.append(cat.catNumber)
        questions = Question.objects.filter(isActive=True, categoryId__catNumber__in=questionCat)
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 10)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        context = {
            "userGroup": userGroup,
            "questionComment": questionComment,
            "category": category,
            "sub": sub,
            "top": top,
            "questions": questions,
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
        }
        return render(request, "ankacademy/question/all-questions.html", context)
    if sub:
        subCat = QuestionCategory.objects.filter(catNumber=sub)
        low = QuestionCategory.objects.filter(isActive=True, parentId__catNumber=sub)
        for getLower in low:
            getLowCategory.append(getLower.catNumber)
        questions = Question.objects.filter(isActive=True, categoryId__catNumber__in=getLowCategory)
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 10)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        context = {
            "userGroup": userGroup,
            "questionComment": questionComment,
            "category": category,
            "low": low,
            "subCat": subCat,
            "sub": sub,
            "questions": questions,
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
        }
        return render(request, "ankacademy/question/all-questions.html", context)
    if lower:
        lowCat = QuestionCategory.objects.filter(catNumber=lower)
        questions = QuestionCategory.objects.filter(isActive=True, categoryId__catNumber=lower)
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 10)
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        context = {
            "userGroup": userGroup,
            "questionComment": questionComment,
            "lowCat": lowCat,
            "lower": lower,
            "questions": questions,
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
        }
        return render(request, "ankacademy/question/all-questions.html", context)
    context = {
        "userGroup": userGroup,
        "topCategories": topCategories,
        "category": category,
        "questions": questions,
        "questionComment": questionComment,
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
    }
    return render(request, "ankacademy/question/all-questions.html", context)


def question_detail(request, slug, postNumber):
    """
    :param request:
    :param slug:
    :param postNumber:
    :return:
    """
    try:
        instance = Question.objects.get(postNumber=postNumber, slug=slug, isActive=True)
    except:
        return redirect("404")
    creatorGroup = current_user_group(request, instance.creator)
    existFollower = get_user_follower(request, request.user, instance.creator)
    articlesCount = user_articles(request, instance.creator).order_by('-createdDate__day')
    questionsCount = user_questions(request, instance.creator).order_by('-createdDate__day')
    coursesCount = user_courses(request, instance.creator).order_by('-createdDate__day')
    examsCount = user_exams(request, instance.creator)
    certifiedAnswersCount = QuestionComment.objects.filter(isCertified=True, isActive=True, creator=instance.creator)
    followers = AccountFollower.objects.filter(followingId__username=instance.creator)
    followings = AccountFollower.objects.filter(followerId__username=instance.creator)
    getFollowerForFollow = get_user_follower(request, request.user, followers)
    getFollowingForFollow = get_user_follower(request, request.user, followings)
    userGroup = current_user_group(request, request.user)
    instance.view += 1
    instance.save()
    reportSubjects = ReportSubject.objects.filter(isActive=True)
    questionAnswers = QuestionComment.objects.filter(questionId__slug=slug, isActive=True,
                                                     questionId__postNumber=postNumber, isRoot=True,
                                                     isReply=False)
    answerReply = QuestionComment.objects.filter(isReply=True, isRoot=False, isActive=True)
    try:
        certifiedAnswer = QuestionComment.objects.get(questionId__slug=slug, isActive=True,
                                                      questionId__postNumber=postNumber, isCertified=True)
    except:
        certifiedAnswer = None
    context = {
        "userGroup": userGroup,
        "creatorGroup": creatorGroup,
        "instance": instance,
        "reportSubjects": reportSubjects,
        "questionAnswers": questionAnswers,
        "certifiedAnswer": certifiedAnswer,
        "answerReply": answerReply,
        "articlesCount": articlesCount,
        "questionsCount": questionsCount,
        "coursesCount": coursesCount,
        "examsCount": examsCount,
        "existFollower": existFollower,
        "getFollowerForFollow": getFollowerForFollow,
        "getFollowingForFollow": getFollowingForFollow,
        "followers": followers,
        "followings": followings,
        "certifiedAnswersCount": certifiedAnswersCount,
    }
    return render(request, "ankacademy/question/question-detail.html", context)


@login_required(login_url="login_account")
def add_report_question(request, postNumber):
    """
    :param postNumber:
    :param request:
    :return:
    """
    try:
        instance = Question.objects.get(postNumber=postNumber)
        if request.method == "POST":
            subjectId = request.POST['subjectId']
            description = request.POST.get("description")
            new_report = Report(subjectId_id=subjectId, description=description, isActive=True, isSolved=False, isRead=False, createdDate=datetime.datetime.now())
            new_report.creatorId = request.user
            new_report.reportNumber = get_random_string(length=32)
            new_report.title = "Kullanıcı Şikayeti"
            new_report.postNumber = postNumber
            new_report.displayMessage = str(new_report.creatorId.get_full_name()) + " adlı kullanıcı soru için şikayette bulundu. Soru numarası: " + postNumber
            new_report.save()
            messages.success(request, "Şikayetiniz başarıyla gönderildi. En kısa sürede tarafınıza geri dönüş sağlanacaktır.")
            return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "postNumber": instance.postNumber}))
        return redirect(reverse("question_detail", kwargs={"slug": instance.slug, "postNumber": instance.postNumber}))
    except:
        messages.error(request, "Soru bulunamadı.")
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
        question = Question.objects.get(postNumber=instance.questionId.postNumber)
        if instance.questionId.creator.username == request.user.username:
            if instance.isCertified:
                instance.isCertified = False
                question.isSolved = False
                instance.save()
                question.save()
                messages.success(request, "Cevabın doğruluğunu iptal ettiniz.")
                return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                   "postNumber": instance.questionId.postNumber}))
            else:
                if question.isSolved:
                    messages.error(request,
                                   "Sorunun, onaylanmış cevabı bulunduğu için, işlem gerçekleştirilemedi. Lütfen önce onayı kaldırın.")
                    return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                       "postNumber": instance.questionId.postNumber}))
                instance.isCertified = True
                question.isSolved = True
                instance.save()
                question.save()
                messages.success(request, "Cevabın doğruluğunu onayladınız.")
                return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                                   "postNumber": instance.questionId.postNumber}))
        else:
            return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                               "postNumber": instance.questionId.postNumber}))
    except:
        return redirect("404")


@login_required(login_url="login_account")
def edit_question(request, postNumber):
    """
    :param request:
    :param postNumber:
    :return:
    """
    try:
        instance = Question.objects.get(postNumber=postNumber)
    except:
        return redirect("404")
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
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
                                    kwargs={"slug": instance.slug, "postNumber": instance.postNumber}))
    else:
        return redirect("401")
    context = {
        "userGroup": userGroup,
        "instance": instance,
        "form": form,
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
    }
    return render(request, "ankacademy/account/post/edit-question.html", context)


@login_required(login_url="login_account")
def add_question_answer(request, slug, postNumber):
    """
    :param request:
    :param slug:
    :param postNumber:
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
        instance = Question.objects.get(slug=slug, postNumber=postNumber)
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
            reverse("question_detail", kwargs={"slug": instance.slug, "postNumber": instance.postNumber}),
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
            reverse("question_detail", kwargs={"slug": instance.questionId.slug, "postNumber": instance.questionId.postNumber}),
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
    try:
        instance = Question.objects.get(slug=slug)
        if instance.creator is request.user:
            if instance.isActive:
                instance.isActive = False
                instance.save()
                messages.success(request, "Soru başarıyla silindi.")
                return redirect("all_questions")
        else:
            return redirect("401")
    except:
        return redirect("404")


@login_required(login_url="login_account")
def delete_question_answer(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        question = Question.objects.get(slug=instance.questionId.slug)
        instance.isActive = False
        instance.updatedDate = datetime.datetime.now()
        if instance.isCertified:
            instance.isCertified = False
        question.view -= 1
        question.save()
        instance.save()
        messages.success(request, "Cevap başarıyla silindi.")
        return redirect(
            reverse("question_detail",
                    kwargs={"slug": instance.questionId.slug, "postNumber": instance.questionId.postNumber}))
    except:
        messages.error(request, "Soru bulunamadı.")
        return redirect("all_questions")


@login_required(login_url="login_account")
def edit_question_answer(request, answerNumber):
    """
    :param request:
    :param answerNumber:
    :return:
    """
    try:
        instance = QuestionComment.objects.get(answerNumber=answerNumber)
        question = Question.objects.get(slug=instance.questionId.slug)
        if request.method == "POST":
            edit = request.POST.get("edit")
            instance.content = edit
            instance.updatedDate = datetime.datetime.now()
            question.view -= 1
            question.save()
            instance.save()
            messages.success(request, "Cevap başarıyla güncellendi.")
        return redirect(
            reverse("question_detail",
                    kwargs={"slug": instance.questionId.slug, "postNumber": instance.questionId.postNumber}))
    except:
        messages.error(request, "Soru bulunamadı.")
        return redirect("all_questions")


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
                                                               "postNumber": instance.questionId.postNumber}))
        else:
            instance.votes.add(user)
            messages.success(request, "Cevap oylamanız başarıyla gerçekleştirildi")
            return redirect(reverse("question_detail", kwargs={"slug": instance.questionId.slug,
                                                               "postNumber": instance.questionId.postNumber}))
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
        postNumber = self.kwargs.get("postNumber")
        obj = get_object_or_404(Question, slug=slug, postNumber=postNumber)
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
        postNumber = self.kwargs.get("postNumber")
        obj = get_object_or_404(QuestionComment, questionId=postNumber)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class QuestionCategoryView(DetailView):

    @staticmethod
    def getTopCategory(request):
        """
        :param request:
        :return topCategory:
        """
        topCategory = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True)|Q(isRoot=True))
        return topCategory

    @staticmethod
    def getSubCategory(request, catNumber):
        """
        :param request:
        :param catNumber:
        :return subCategory:
        """
        instance = get_object_or_404(QuestionCategory, catNumber=catNumber)
        subCategory = QuestionCategory.objects.filter(parentId__catNumber=instance)
        return subCategory

    @staticmethod
    def getLowCategory(request, catNumber):
        """
        :param request:
        :return catNumber:
        """
        instance = get_object_or_404(QuestionCategory, catNumber=catNumber)
        lowCategory = QuestionCategory.objects.filter(parentId__catNumber=instance.catNumber)
        return lowCategory