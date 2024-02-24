from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from emailing.models import Subscriber, MailingList
from emailing.serializers import CreateMailingListSerializer, SubscriberSerializer, MessageSerializer
from users.models import CustomUser


class CreateMailingList(APIView):
    serializer_class = CreateMailingListSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                if isinstance(request.user, CustomUser):
                    name = serializer.validated_data.get('name')
                    if name:
                        serializer.save(created_by=request.user)
                        return Response({"Message": f"Mailing list '{name}' create"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"error": "Name field is required."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "You are not authorized to create mailing lists."},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Request is messing from serializer context'})


class AddSubscriber(APIView):
    serializer_class = SubscriberSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request, 'user': request.user})
            serializer.is_valid(raise_exception=True)
            emails = serializer.validated_data.get('emails')
            mailing_list_name = serializer.validated_data.get('mailing_list')
            try:
                mailing_list = MailingList.objects.get(name=mailing_list_name, created_by=request.user)
            except MailingList.DoesNotExist:
                return Response(
                    {'Error': f"Mailing list '{mailing_list_name}' does not exist or you don't have access to it."},
                    status=status.HTTP_404_NOT_FOUND)
            existing_emails = Subscriber.objects.filter(email__in=emails, mailing_list=mailing_list).values_list(
                'email', flat=True)
            exist_emails = [email for email in emails if email in existing_emails]
            if exist_emails:
                return Response({
                    'Error': f"{exist_emails} emails exist in the mailing list: {mailing_list}."},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'Message': f'Emails: {emails}, have been added to the mailing list: {mailing_list_name}'},
                status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendMessage(APIView):
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subject = request.POST.get('subject')
            text = request.POST.get('text')
            from_email = request.POST.get('from_email')
            recipient_list = request.POST.getlist('recipient_list', [])

            send_mail(subject, text, from_email, recipient_list)

            return Response({'message': 'Emailurile au fost trimise cu succes!'})
        else:
            return Response({'error': 'Doar metoda POST este acceptată pentru acest endpoint!'}, status=400)


class RemoveSubscriber(APIView):
    ...


class AllListMailing(APIView):
    ...


class AllUsersMailingList(APIView):
    ...
