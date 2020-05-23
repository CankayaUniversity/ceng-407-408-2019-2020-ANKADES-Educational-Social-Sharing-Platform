import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.signals import pre_save
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.generic import DetailView

from ankadescankaya.slug import slug_save
from ankadescankaya.views.views import current_user_group
from question.forms import EditQuestionForm
from question.models import QuestionCategory, Question


@login_required(login_url="login_admin")
def admin_add_question_category(request):
    """
    :param request:
    :return:
    """
    topCategory = QuestionCategoryView.getTopCategory(request)
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "topCategory": topCategory
    }
    if userGroup == 'admin' or userGroup == 'moderator':
        getTop = request.GET.get('getTop')
        postTop = request.POST.get('postTop')
        home = request.POST.get('home')
        if getTop or home or postTop:
            if home:  # If request category slug is equal to home
                parent = QuestionCategory.objects.get(catNumber=home)
                if request.method == 'POST':
                    title = request.POST.get('title')
                    isActive = request.POST.get("isActive") == 'on'
                    new_cat = QuestionCategory(creator=request.user, isCategory=True, isActive=isActive, isRoot=False,
                                             parentId=parent, title=title)
                    new_cat.catNumber = "q-" + get_random_string(length=7)
                    new_cat.createdDate = datetime.datetime.now()
                    new_cat.creator = request.user
                    new_cat.save()
                    messages.success(request, "Soru için üst kategori başarıyla eklendi.")
                    return redirect("admin_add_question_category")
            if getTop == 'q-jOuLKTg':
                home = QuestionCategory.objects.get(catNumber=getTop)
                context = {
                    "getTop": getTop,
                    "userGroup": userGroup,
                    "home": home
                }
                return render(request, "adminpanel/question/add-category.html", context)
            if postTop:
                inputTop = QuestionCategory.objects.get(catNumber=postTop)
                selectSub = QuestionCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                if request.method == 'POST':
                    selection = request.POST.get('selection')
                    if selection == 'none':
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_top = QuestionCategory(title=title, isCategory=True, isActive=isActive, isRoot=False,
                                                 parentId=inputTop)
                        new_top.catNumber = "q-" + get_random_string(length=7)
                        new_top.createdDate = datetime.datetime.now()
                        new_top.creator = request.user
                        new_top.save()
                        messages.success(request, "Alt kategori başarıyla eklendi.")
                        return redirect("admin_add_question_category")
                    else:
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_lower = QuestionCategory(title=title, isCategory=True, isActive=isActive, isRoot=False,
                                                   parentId=inputTop)
                        new_lower.catNumber = "q-" + get_random_string(length=7)
                        new_lower.createdDate = datetime.datetime.now()
                        new_lower.creator = request.user
                        new_lower.save()
                        messages.success(request, "En alt kategori başarıyla eklendi.")
                        return redirect("admin_add_question_category")
                return render(request, "adminpanel/question/add-category.html", context)
            else:
                inputTop = QuestionCategory.objects.get(catNumber=getTop)
                selectSub = QuestionCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                return render(request, "adminpanel/question/add-category.html", context)
        else:
            return render(request, "adminpanel/question/add-category.html", context)
    else:
        return redirect("index")


@login_required(login_url="login_admin")
def admin_edit_question_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=True)).order_by('title')
    userGroup = current_user_group(request, request.user)
    try:
        instance = QuestionCategory.objects.get(slug=slug)
        if userGroup == 'admin' or userGroup == "moderator":
            if request.method == "POST":
                value = request.POST['categoryId']
                title = request.POST.get("title")
                isActive = request.POST.get("isActive") == "on"
                isCategory = request.POST.get("isCategory") == "on"
                if instance.parentId_id != value:
                    instance.parentId_id = value
                    instance.title = title
                    instance.isActive = isActive
                    instance.isCategory = isCategory
                    pre_save.connect(slug_save, sender=QuestionCategory)
                    instance.save()
                    messages.success(request, "Soru kategorisi başarıyla güncellendi.")
                    return redirect("admin_question_categories")
                messages.error(request, "Eklemek istediğiniz kategori zaten mevcut.")
                return redirect("admin_question_categories")
            context = {
                "userGroup": userGroup,
                "questionCategory": questionCategory,
                "instance": instance,
            }
            return render(request, "adminpanel/question/edit-category.html", context)
    except:
        messages.error(request, "Soru kategorisi bulunamadı.")
        return redirect("admin_question_categories")


@login_required(login_url="login_admin")
def admin_question_categories(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = QuestionCategory.objects.all()
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=True))
    questionCategoryLimit = QuestionCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "questionCategory": questionCategory,
        "questionCategoryLimit": questionCategoryLimit,
    }
    return render(request, "adminpanel/question/categories.html", context)


@login_required(login_url="login_admin")
def admin_delete_question_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = QuestionCategory.objects.get(slug=slug)
        if instance.isActive is True:
            messages.error(request, "Soru kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_question_categories")
        else:
            instance.delete()
            messages.success(request, "Soru kategorisi başarıyla silindi.")
            return redirect("admin_question_categories")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_isactive_question(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = Question.objects.get(slug=slug)
        userGroup = current_user_group(request, request.user)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Soru kategorisi artık aktif değil.")
                return redirect("admin_all_questions")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Soru başarıyla aktifleştirildi.")
                return redirect("admin_all_questions")
        else:
            messages.error(request, "Yetkiniz Yok")
            return redirect("admin_all_questions")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_isactive_question_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    try:
        instance = QuestionCategory.objects.get(slug=slug)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Soru kategorisi artık aktif değil.")
                return redirect("admin_question_categories")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Soru kategorisi başarıyla aktifleştirildi.")
                return redirect("admin_question_categories")
        else:
            messages.error(request, "Yetkiniz Yok")
            return redirect("admin_question_categories")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_delete_question(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        instance = get_object_or_404(Question, slug=slug)
        if instance.isActive is True:
            messages.error(request, "Soru aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_all_questions")
        else:
            instance.delete()
            messages.success(request, "Soru başarıyla silindi.")
            return redirect("admin_all_questions")
    else:
        messages.error(request, "Yetkiniz Yok")
        return redirect("admin_all_questions")


@login_required(login_url="login_admin")
def admin_all_questions(request):
    """
    :param request:
    :return:
    """
    questions = Question.objects.all()
    userGroup = current_user_group(request, request.user)
    context = {
        "questions": questions,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/question/all-questions.html", context)


@login_required(login_url="login_admin")
def admin_edit_question(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=False))
    instance = Question.objects.get(slug=slug)
    form = EditQuestionForm(request.POST or None, instance=instance)
    context = {
        "questionCategory": questionCategory,
        "userGroup": userGroup,
        "form": form,
        "instance": instance,
    }
    if request.method == "POST":
        value = request.POST['categoryId']
        title = request.POST.get("title")
        isActive = request.POST.get("isActive") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        instance.isActive = isActive
        instance.title = title
        instance.categoryId_id = value
        instance.isActive = isActive
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Soru başarıyla düzenlendi !")
        return redirect("admin_all_questions")
    return render(request, "adminpanel/question/edit-question.html", context)


class QuestionCategoryView(DetailView):

    @staticmethod
    @login_required(login_url="login_admin")
    def getTopCategory(request):
        """
        :param request:
        :return topCategory:
        """
        topCategory = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True)|Q(isRoot=True))
        return topCategory

    @staticmethod
    @login_required(login_url="login_admin")
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
    @login_required(login_url="login_admin")
    def getLowCategory(request, catNumber):
        """
        :param request:
        :return catNumber:
        """
        instance = get_object_or_404(QuestionCategory, catNumber=catNumber)
        lowCategory = QuestionCategory.objects.filter(parentId__catNumber=instance)
        return lowCategory
