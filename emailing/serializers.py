from rest_framework import serializers

from emailing.models import MailingList, Subscriber, Message


class CreateMailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ['name', 'created_by']


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'mailing_list']
