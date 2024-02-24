from django.db import models
from users.models import CustomUser


class MailingList(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Subscriber(models.Model):
    email = models.EmailField()
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.email}' is in mailing list: {self.mailing_list}"


class Message(models.Model):
    subject = models.CharField(max_length=100)
    text = models.TextField()
    from_email = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'Subject: {self.subject}, text: {self.text}, from_email: {self.from_email}, Timestamp: {self.timestamp}')
