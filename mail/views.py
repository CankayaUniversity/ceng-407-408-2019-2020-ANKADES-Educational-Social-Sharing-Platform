from django.shortcuts import render
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from mail.models import Mail


def inbox(request):
    return None


def send_mail(request):
    randomString = get_random_string(length=32)


# class MailAPI(APIView):
#
#     @swagger_auto_schema(operation_summary="Admin activate or deactivate the groups")
#     def get(self, request, messageNumber=None, format=None):
#         slug = self.kwargs.get("slug")
#         obj = get_object_or_404(Mail, slug=slug)
#         updated = False
#         isActivated = False
#         if obj.isActive is True:
#             isActivated = False
#             obj.isActive = False
#             obj.updatedDate = datetime.datetime.now()
#             obj.save()
#             updated = True
#         else:
#             isActivated = True
#             obj.isActive = True
#             obj.updatedDate = datetime.datetime.now()
#             obj.save()
#             updated = True
#         data = {
#             "updated": updated,
#             "isActivated": isActivated
#         }
#         return Response(data)