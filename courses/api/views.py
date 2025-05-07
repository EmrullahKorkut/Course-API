from urllib import response
from django.forms import ValidationError
from rest_framework import generics, viewsets, mixins, permissions, status
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework.decorators import action

from django.shortcuts import get_object_or_404


from courses.api.permissions import IsAdminOrReadOnly, IsAdminOrTeacherOrReadOnly, IsStudentOrReadOnly


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


class LessonListCreateView(generics.ListCreateAPIView):
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

class CartAddDeleteView(APIView):
    permission_classes = [IsStudentOrReadOnly]

    def post(self, request, pk):
        user = request.user
        cart = Cart.objects.get(student=user)
        course = get_object_or_404(Course, pk=pk)

        if course in cart.courses.all():
            return Response(
                {"message": "You cant add the same course!!.."}, 
                status=status.HTTP_200_OK)
        
        cart.courses.add(course)

        return Response({
            "message": f"The course '{course.title}' added to cart!! Pay the money and use the courses"
        }, 
        status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = request.user
        cart = get_object_or_404(Cart, student=user)
        course = get_object_or_404(Course, pk=pk)

        if course not in cart.courses.all():
            return Response(
                {"message": "Course not in your cart you can add the course"}, 
                status=status.HTTP_404_NOT_FOUND)

        cart.courses.remove(course)
        return Response({"message": f"'{course.title} removed from cart!!"}, status=status.HTTP_200_OK)


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    lookup_field = 'student__username'
    permission_classes = [IsStudentOrReadOnly]

    def get_object(self):
        username = self.kwargs.get('student')
        try:
            cart = Cart.objects.get(student__username=username)
        except Cart.DoesNotExist:
            raise NotFound('There is no a cart for you.please add a course to the card')

        return cart

#-----------------------------------------------------------------------------------------------

# class CartContentListView(generics.ListAPIView):
#     queryset = CartContent.objects.all()
#     serializer_class = CartContentSerializer
#     permission_classes = []

#-----------------------------------------------------------------------------------------------

class PaymentView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = []

#-----------------------------------------------------------------------------------------------

class EnrollListView(generics.ListAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = []


#-----------------------------------------------------------------------------------------------

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []

#-----------------------------------------------------------------------------------------------

class LikeListView(generics.ListAPIView):
    queryset = ReviewLike.objects.all()
    serializer_class = LikeSerializer
    permission_classes = []

#-----------------------------------------------------------------------------------------------

class FavouriteListView(generics.ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = []

#-----------------------------------------------------------------------------------------------