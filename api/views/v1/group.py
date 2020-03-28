import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Group


class IsActiveGroupAPIToggle(APIView):

    @swagger_auto_schema(operation_summary="Admin activate or deactivate the groups")
    def get(self, request, slug=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Group, slug=slug)
        updated = False
        isActivated = False
        if obj.isActive is True:
            isActivated = False
            obj.isActive = False
            obj.updatedDate = datetime.datetime.now()
            obj.save()
            updated = True
        else:
            isActivated = True
            obj.isActive = True
            obj.updatedDate = datetime.datetime.now()
            obj.save()
            updated = True
        data = {
            "updated": updated,
            "isActivated": isActivated
        }
        return Response(data)