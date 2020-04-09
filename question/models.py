import uuid
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save


class QuestionCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    isRoot = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "QuestionCategory"
        ordering = ['-createdDate']


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    introduction = models.CharField(null=True, blank=True, max_length=254)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    categoryId = models.ForeignKey(QuestionCategory, on_delete=models.PROTECT, null=False)
    title = models.CharField(max_length=254, null=False, blank=False)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField(null=False, blank=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    likes = models.ManyToManyField(Account, related_name="questionLikes", default=0, blank=True,
                                   db_table="LikedQuestion")

    def __str__(self):
        return self.questionNumber

    def __unicode__(self):
        return self.questionNumber

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"slug": self.slug, "questionNumber": self.questionNumber})

    def get_like_url(self):
        return reverse("question-like-toggle", kwargs={"slug": self.slug, "questionNumber": self.questionNumber})

    def get_api_like_url(self):
        return reverse("question-like-api-toggle", kwargs={"slug": self.slug, "questionNumber": self.questionNumber})

    class Meta:
        db_table = "Question"
        ordering = ['-createdDate']


class QuestionComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionId = models.ForeignKey(Question, on_delete=models.PROTECT)
    answerNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, related_name="questionCommentId", on_delete=models.PROTECT)
    isRoot = models.BooleanField(default=True)
    isCertified = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    isReply = models.BooleanField(default=False)
    view = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(Account, related_name="questionCommentLikes", default=0, blank=True, db_table="LikedQuestionComment")

    def __str__(self):
        return self.answerNumber

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"slug": self.questionId.slug, "questionNumber": self.questionId.questionNumber})

    def get_like_url(self):
        return reverse("question-like-comment-toggle", kwargs={"questionNumber": self.answerNumber})

    def get_api_like_url(self):
        return reverse("question-like-comment-api-toggle", kwargs={"questionNumber": self.answerNumber})

    class Meta:
        db_table = "QuestionComment"
        ordering = ['-createdDate']


pre_save.connect(slug_save, sender=Question)
pre_save.connect(slug_save, sender=QuestionCategory)