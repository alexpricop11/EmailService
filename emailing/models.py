from django.db import models

from users.models import CustomUser


class MailingList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} created by {self.created_by}"


class Subscriber(models.Model):
    email = models.EmailField()
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} is in |{self.mailing_list}|"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Sender: {self.sender}, Mailing: {self.mailing_list}, Subject: {self.subject},Text: {self.body}'
                f' Timestamp: {self.timestamp}')
