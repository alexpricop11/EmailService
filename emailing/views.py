from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from emailing.serializers import CreateMailingListSerializer


class CreateMailingList(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = CreateMailingListSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            if name:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSubscriber(APIView):
    ...


class SendMessage(APIView):
    ...


class RemoveSubscriber(APIView):
    ...


class AllListMailing(APIView):
    ...


class AllUsersMailingList(APIView):
    ...
