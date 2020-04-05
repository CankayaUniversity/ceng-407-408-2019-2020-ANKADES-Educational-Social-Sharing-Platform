import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from account.models import AccountGroup
from account.views.views import current_user_group
from adminpanel.models import AdminActivity
from question.models import QuestionCategory, Question


@login_required(login_url="login_admin")
def admin_add_question_category(request):
    """
    :param request:
    :return:
    """
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=True))
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "questionCategory": questionCategory,
    }
    if userGroup == 'admin':
        if request.method == "POST":
            categoryId = request.POST.get("categoryId")
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            try:
                getTitle = QuestionCategory.objects.get(title=title)
                if title:
                    error = title + " isimli kategori " + getTitle.parentId.title + " kategorisinde zaten mevcut."
                    messages.error(request, error)
                    return redirect("admin_add_question_category")
            except:
                instance = QuestionCategory(parentId_id=categoryId, title=title, isActive=isActive,
                                            isCategory=isCategory)
                instance.creator = request.user
                instance.save()
                activity.title = "Soru Kategorisi Ekleme: " + str(currentUser)
                activity.application = "Question"
                activity.createdDate = datetime.datetime.now()
                activity.method = "POST"
                activity.creator = currentUser
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı sorular için kategori ekledi."
                activity.save()
                messages.success(request, "Soru kategorisi başarıyla eklendi !")
                return redirect("admin_question_categories")
        return render(request, "adminpanel/question/add-category.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_question_categories(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    categories = QuestionCategory.objects.all()
    questionCategory = QuestionCategory.objects.filter(Q(isActive=True, isCategory=True))
    questionCategoryLimit = QuestionCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "questionCategory": questionCategory,
        "questionCategoryLimit": questionCategoryLimit,
        "currentUser": currentUser,
    }
    return render(request, "adminpanel/question/categories.html", context)


@login_required(login_url="login_admin")
def admin_delete_article_category(request, slug):
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
        currentUser = request.user
        userGroup = current_user_group(request, currentUser)
        activity = AdminActivity()
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.save()
                activity.title = "Soru Aktifleştirme"
                activity.application = "Question"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı soru aktifliğini kaldırdı."
                activity.save()
                messages.success(request, "Soru kategorisi artık aktif değil.")
                return redirect("admin_all_questions")
            else:
                instance.isActive = True
                instance.save()
                activity.title = "Soru Aktifleştirme"
                activity.application = "Question"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı soru aktifleştirdi."
                activity.save()
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
    try:
        instance = QuestionCategory.objects.get(slug=slug)
        currentUser = request.user
        userGroup = current_user_group(request, currentUser)
        activity = AdminActivity()
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.save()
                activity.title = "Soru Kategorisini Aktifleştirme"
                activity.application = "Question"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı soru kategorisinin aktifliğini kaldırdı."
                activity.save()
                messages.success(request, "Soru kategorisi artık aktif değil.")
                return redirect("admin_question_categories")
            else:
                instance.isActive = True
                instance.save()
                activity.title = "Soru Kategorisini Aktifleştirme"
                activity.application = "Question"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı soru kategorisinin aktifleştirdi."
                activity.save()
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
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if userGroup == 'admin':
        instance = get_object_or_404(Question, slug=slug)
        if instance.isActive is True:
            activity.title = "Soru Silme"
            activity.application = "Question"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı soru silme işleminde bulundu. Başarısız."
            activity.save()
            messages.error(request, "Soru aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_question_categories")
        else:
            instance.delete()
            activity.title = "Soru Silme"
            activity.application = "Question"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı soru sildi."
            activity.save()
            messages.success(request, "Soru başarıyla silindi.")
            return redirect("admin_all_questions")
    else:
        messages.error(request, "Yetkiniz Yok")
        return redirect("admin_all_questions")


@login_required(login_url="login_admin")
def admin_delete_question_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if userGroup == 'admin':
        instance = get_object_or_404(QuestionCategory, slug=slug)
        if instance.isActive is True:
            activity.title = "Soru Kategori Silme"
            activity.application = "Question"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı soru kategorisini silme işleminde bulundu. Başarısız."
            activity.save()
            messages.error(request, "Soru kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_question_categories")
        else:
            instance.delete()
            activity.title = "Soru Kategori Silme"
            activity.application = "Question"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı soru kategorisini sildi."
            activity.save()
            messages.success(request, "Soru kategorisi başarıyla silindi.")
            return redirect("admin_question_categories")
    else:
        messages.error(request, "Yetkiniz Yok")
        return redirect("admin_question_categories")


@login_required(login_url="login_admin")
def admin_all_questions(request):
    """
    :param request:
    :return:
    """
    questions = Question.objects.all()
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "questions": questions,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/question/all-questions.html", context)
