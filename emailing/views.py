from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from emailing.serializers import CreateMailingListSerializer
from users.models import CustomUser


class CreateMailingList(APIView):
    serializer_class = CreateMailingListSerializer

    @login_required
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if isinstance(request.user, CustomUser):
                name = serializer.validated_data.get('name_list')
                if name:
                    serializer.save(created_by=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Name field is required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
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
