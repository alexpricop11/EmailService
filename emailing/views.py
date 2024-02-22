from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from emailing.serializers import CreateMailingListSerializer, SubscriberSerializer
from users.models import CustomUser


class CreateMailingList(APIView):
    serializer_class = CreateMailingListSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if isinstance(request.user, CustomUser):
                name = serializer.validated_data.get('name')
                if name:
                    serializer.save(created_by=request.user)
                    return Response({"Message": "This mailing create"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Name field is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSubscriber(APIView):
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class SendMessage(APIView):
    ...


class RemoveSubscriber(APIView):
    ...


class AllListMailing(APIView):
    ...


class AllUsersMailingList(APIView):
    ...
