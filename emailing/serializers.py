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
    emails = serializers.CharField(required=True)

    class Meta:
        model = Subscriber
        fields = ['emails', 'mailing_list']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['mailing_list'].queryset = MailingList.objects.filter(created_by=request.user)

    @staticmethod
    def validate_emails(value):
        emails = [email.strip() for email in value.split(',') if email.strip()]
        for email in emails:
            if not serializers.EmailField().run_validation(email):
                raise serializers.ValidationError(f"{email} is not a valid email address.")
        return emails

    def create(self, validated_data):
        mailing_list = MailingList.objects.get(name=validated_data['mailing_list'],
                                               created_by=self.context['request'].user)
        emails = validated_data.pop('emails')
        subscribers = []
        for email in emails:
            subscriber = Subscriber.objects.create(email=email, mailing_list=mailing_list)
            subscribers.append(subscriber)
        return subscribers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['subject', 'text', 'from_email', 'timestamp']
