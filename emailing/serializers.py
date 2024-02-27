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
        fields = ['subject', 'text', 'mailing_list', 'timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['mailing_list'].queryset = MailingList.objects.filter(created_by=request.user)


class RemoveSubscriberSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(slug_field='email', queryset=Subscriber.objects.all())

    class Meta:
        model = Subscriber
        fields = ['email', 'mailing_list']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['mailing_list'].queryset = MailingList.objects.filter(created_by=request.user)

    def delete_subs(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['email'].queryset = Subscriber.objects.filter(email=request.email)


class AllListMailingSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = MailingList
        fields = ['name', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class AllUsersMailingListSerializer(serializers.ModelSerializer):
    mailing_list = serializers.CharField(source='mailing_list.name', read_only=True)
    subscribers = serializers.SerializerMethodField(source='email')

    class Meta:
        model = MailingList
        fields = ['mailing_list', 'subscribers']

    @staticmethod
    def get_subscribers(obj):
        subscriber = Subscriber.objects.filter(mailing_list=obj.mailing_list).values_list('email', flat=True)
        subscribers = list(set(subscriber))
        return subscribers


class EmailsSentSerializer(serializers.ModelSerializer):
    mailing_list = serializers.CharField(source='mailing_list.name', read_only=True)

    class Meta:
        model = Message
        fields = ['subject', 'mailing_list']
