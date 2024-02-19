from rest_framework import serializers

from emailing.models import MailingList, Subscriber, Message


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ['name', 'created_by']


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'mailing_list', 'subject', 'body', 'timestamp']
