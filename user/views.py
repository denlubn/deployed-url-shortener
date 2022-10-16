from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer


class CreateUserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "registration/sign_up.html"

    def get(self, request):
        serializer = UserSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('user:token_obtain_pair')


class ManageUserView(APIView):
    permission_classes = (IsAuthenticated,)

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "user/user_detail.html"

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response({'serializer': serializer, 'user': user})

    def post(self, request):  # same as partial_update
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('user:manage')
