from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

from emailing.models import Subscriber
from emailing.serializers import CreateMailingListSerializer, SubscriberSerializer, MessageSerializer
from users.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


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
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data.get('email')
                mail_list = serializer.validated_data.get('mailing_list')
                if email and mail_list:
                    serializer.save()
                    return Response({'Message': f'Email: {email}, has been added to the in {mail_list}'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'Error': 'Field is required.'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Request is messing from serializer context'},
                            status=status.HTTP_400_BAD_REQUEST)


class SendMessage(APIView):
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject'],
            text = serializer.validated_data['text'],
            from_email = [email for email in 'mailing_list']
            sent_mail = send_mail(
                subject,
                text,
                from_email
            )
            return Response({'Message': sent_mail}, status=status.HTTP_200_OK)
        return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RemoveSubscriber(APIView):
    ...


class AllListMailing(APIView):
    ...


class AllUsersMailingList(APIView):
    ...
