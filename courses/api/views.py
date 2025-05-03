from rest_framework import generics

from courses.api.serializers import RegisterSerializer
from courses.models import User

from rest_framework.permissions import IsAdminUser


class RegisterView(generics.CreateAPIView):  #yazdığımız user modeline kayıt işlemi
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []



