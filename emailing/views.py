from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from emailing.models import Subscriber, MailingList, Message
from emailing.serializers import CreateMailingListSerializer, SubscriberSerializer, MessageSerializer, \
    RemoveSubscriberSerializer, AllListMailingSerializer, AllUsersMailingListSerializer, EmailsSentSerializer


class BaseAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CreateMailingList(BaseAPIView):
    serializer_class = CreateMailingListSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            name = serializer.validated_data.get('name')
            serializer.save(created_by=request.user)

            return Response({"Message": f"Mailing list '{name}' created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error': str({e})})


class AddSubscriber(BaseAPIView):
    serializer_class = SubscriberSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request, 'user': request.user})
            serializer.is_valid(raise_exception=True)
            emails = serializer.validated_data.get('emails')
            mailing_list_name = serializer.validated_data.get('mailing_list')
            mailing_list = MailingList.objects.get(name=mailing_list_name, created_by=request.user)
            existing_emails = Subscriber.objects.filter(email__in=emails, mailing_list=mailing_list).values_list(
                'email',
                flat=True)
            exist_emails = [email for email in emails if email in existing_emails]
            if exist_emails:
                return Response({'Error': f"{exist_emails} emails exist in the mailing list: {mailing_list}."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'Message': f'Emails: {emails}, have been added to the mailing list: {mailing_list_name}'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str({e})})


class SendMessage(BaseAPIView):
    serializer_class = MessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            subject = serializer.validated_data.get('subject')
            text = serializer.validated_data.get('text')
            mailing_list = serializer.validated_data.get('mailing_list')
            try:
                mailing_list = MailingList.objects.get(name=mailing_list, created_by=request.user)
                subscribers = Subscriber.objects.filter(mailing_list=mailing_list)
                recipient_list = [subscriber.email for subscriber in subscribers]
                send_mail(subject, text, mailing_list.name, recipient_list)
                Message.objects.create(
                    subject=subject,
                    mailing_list=mailing_list,
                )
                return Response({"Success": "The message was sent."}, status=status.HTTP_200_OK)
            except MailingList.DoesNotExist:
                return Response({'Error': "This mailing list does not exist or does not belong to the current user."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveSubscriber(BaseAPIView):
    serializer_class = RemoveSubscriberSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            mailing_list = serializer.validated_data.get('mailing_list')
            email.delete()
            return Response({"Message": f"Subscriber has been deleted from {mailing_list}."},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error': str({e})})


class AllListMailing(BaseAPIView):
    serializer_class = AllListMailingSerializer

    def get(self, request):
        try:
            list_mailing = MailingList.objects.filter(created_by=request.user)
            serializer = self.serializer_class(list_mailing, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error': str({e})})


class AllUsersMailingList(BaseAPIView):
    serializer_class = AllUsersMailingListSerializer

    def get(self, request):
        try:
            list_subscriber = Subscriber.objects.filter(mailing_list__created_by=request.user)
            subscribers = list({subscriber.mailing_list.id: subscriber for subscriber in list_subscriber}.values())
            serializer = self.serializer_class(subscribers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error': str({e})})


class EmailSent(APIView):
    serializer_class = EmailsSentSerializer

    @staticmethod
    def get(request):
        try:
            sent_emails = Message.objects.filter(mailing_list__created_by=request.user).order_by('-timestamp')
            serializer = EmailsSentSerializer(sent_emails, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error': str({e})})
