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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['mailing_list'].queryset = MailingList.objects.filter(created_by=request.user)

    def create(self, validated_data):
        validated_data['mailing_list'] = MailingList.objects.get(pk=validated_data['mailing_list'],
                                                                 created_by=self.context['request'].user)
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['subject', 'text', 'from_email', 'timestamp']
