from rest_framework import generics

from courses.api.serializers import RegisterSerializer, CategorySerializer, CourseSerializer, LessonSerializer, EnrollSerializer, CartSerializer, CartContentSerializer, PaymentSerializer, ReviewSerializer, LikeSerializer, FavouriteSerializer
from courses.models import User, Category, Course, Lesson, Enroll, Cart, CartContent, Payment, Review, ReviewLike, Favourite

from rest_framework.permissions import IsAdminUser


# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins


class RegisterView(generics.CreateAPIView):  #yazdığımız user modeline kayıt işlemi
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  

#---------------------------------------------------deneme için listeleme views, Viewsetlere geçilecek routerlar ayarlanacak---------------------------

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []



class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = []



class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = []



class EnrollListView(generics.ListAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = []



class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = []



class CartContentListView(generics.ListAPIView):
    queryset = CartContent.objects.all()
    serializer_class = CartContentSerializer
    permission_classes = []



class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
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
