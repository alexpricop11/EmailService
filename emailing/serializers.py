from rest_framework import serializers

from emailing.models import MailingList, Subscriber, Message


class CreateMailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ['name']

    name = serializers.CharField(required=True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'mailing_list']
