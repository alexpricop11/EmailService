from django.urls import path

from emailing.views import CreateMailingList, AddSubscriber

urlpatterns = [
    path("create/", CreateMailingList.as_view()),
    path("add-subs/", AddSubscriber.as_view()),
]
