from django.urls import path

from emailing.views import CreateMailingList

urlpatterns = [
    path("create/", CreateMailingList.as_view()),
]
