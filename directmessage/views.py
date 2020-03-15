import datetime
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404

from account.models import Account
from directmessage.forms import MessageForm
from directmessage.models import DirectMessage


@login_required(login_url="login_account")
def send_direct_message(request, username):
    instance = get_object_or_404(Account, username=username)
    if request.method == "POST":
        message = request.POST.get("message")
        new_message = DirectMessage(message=message)
        new_message.creator = request.user
        new_message.user = instance
        new_message.isTicket = True
        rnd = random.randrange(1, 2147483647)
        while DirectMessage.objects.filter(messageNumber__exact=rnd):
            rnd = random.randrange(1, 2147483647)
        new_message.messageNumber = rnd
        new_message.updatedDate = datetime.datetime.now()
        new_message.isBlocked = False
        new_message.isRead = False
        new_message.isReply = False
        new_message.isRoot = False
        new_message.save()
        messages.success(request, "Gönderildi")
    return redirect(reverse("direct_message_detail", kwargs={"username": username}))


@login_required(login_url="login_admin")
def direct_message_detail(request, username):
    instance = get_object_or_404(Account, username=username)
    message = DirectMessage.objects.filter(Q(user__username=username))
    messages.isRead = True
    context = {
        "message": message,
        "instance": instance,
        "instance.username": instance.username,
        "instance.first_name": instance.first_name,
        "instance.last_name": instance.last_name,
    }
    return render(request, "ankades/directmessage/message-detail.html", context)

@login_required(login_url="login_admin")
def block_direct_message(request, messageNumber):
    instance = get_object_or_404(DirectMessage, messageNumber=messageNumber)
    instance.isBlocked = True
    instance.save()
    messages.success(request, "Mesaj engellendi")
    return redirect("my_direct_messages_list")


@login_required(login_url="login_admin")
def delete_direct_message(request, messageNumber):
    instance = get_object_or_404(DirectMessage, messageNumber=messageNumber)
    instance.isDeleted = True
    instance.save()
    messages.success(request, "Mesaj silindi")
    return redirect("my_direct_messages_list")


@login_required(login_url="login_admin")
def my_direct_messages_list(request, username):
    user = get_object_or_404(Account, username=username)
    getMessages = DirectMessage.objects.filter(Q(creator=user, isDeleted=False))
    context = {
        "getMessages": getMessages,
    }
    return render(request, "ankades/directmessage/my-messages-list.html", context)


class LikeDirectMessage(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        message = self.kwargs.get("message")
        obj = get_object_or_404(DirectMessage, message=message)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_