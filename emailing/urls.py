from django.urls import path

from emailing.views import CreateMailingList, AddSubscriber, SendMessage

urlpatterns = [
    path("create-list/", CreateMailingList.as_view()),
    path("add-subs/", AddSubscriber.as_view()),
    path("send-mail/", SendMessage.as_view()),
]
