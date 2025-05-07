from urllib import response
from django.forms import ValidationError
from rest_framework import generics, viewsets, mixins, permissions, status
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.decorators import action

from django.shortcuts import get_object_or_404


from courses.api.permissions import IsAdminOrReadOnly, IsAdminOrTeacherOrReadOnly


from courses.api.serializers import (
    RegisterSerializer, 
    CategorySerializer, 
    CourseSerializer, 
    LessonSerializer, 
    EnrollSerializer, 
    CartSerializer, 
    PaymentSerializer, 
    ReviewSerializer, 
    LikeSerializer, 
    FavouriteSerializer,
    UserSerializer
    )
from courses.models import User, Category, Course, Lesson, Enroll, Cart, Payment, Review, ReviewLike, Favourite



# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins


class RegisterView(generics.CreateAPIView):  #yazdığımız user modeline kayıt işlemi
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  

#---------------------------------------------------deneme için listeleme views, crud işlemlerine geçilecek routerlar, urller ayarlanacak---------------------------
#--------------------------------------------------------------------------------------------
class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):                                #USER LİSTELEMESİ VE DETAYLARI
        return self.list(request, *args, **kwargs)                                          
    
class UserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
#-----------------------------------------------------------------------------------------------

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()                                   #CATEGORY VİEW. NOT SAFE METODLAR SADECE ADMİN İÇİNDİR. LİST RETRİEVE AUTH USERS İÇİN
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


#------------------------------------------------------------------------------------------------

class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()                                     #ADMİN TEACHER EDİTLER KALANLAR SADECE LİST EDER
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

#------------------------------------------------------------------------------------------------

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = []

    def get_queryset(self):
        course_id = self.kwargs['pk']
        course = get_object_or_404(Course, pk=course_id)
        return Lesson.objects.filter(course=course)
    
class LessonDetailView(generics.RetrieveAPIView):                           #
    serializer_class = LessonSerializer

    def get_object(self):   
        course_id = self.kwargs['pk']
        lesson_id = self.kwargs['lesson_id']
        course = get_object_or_404(Course, pk=course_id)
        lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
        return lesson


#-----------------------------------------------------------------------------------------------


class CartAddView():
    pass


#-----------------------------------------------------------------------------------------------

# class CartContentListView(generics.ListAPIView):
#     queryset = CartContent.objects.all()
#     serializer_class = CartContentSerializer
#     permission_classes = []



class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = []


class EnrollListView(generics.ListAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = []



class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []



class LikeListView(generics.ListAPIView):
    queryset = ReviewLike.objects.all()
    serializer_class = LikeSerializer
    permission_classes = []



class FavouriteListView(generics.ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = []
