from rest_framework import serializers

from courses.models import User, Category, Course, Lesson, Enroll, Cart, Payment, Review, ReviewLike, Favourite


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_teacher']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_teacher=validated_data.get('is_teacher', False),
            is_student=not validated_data.get('is_teacher', False)
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_teacher']
    


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
    )
    
    class Meta:
        model = Course
        fields = '__all__'


    
class CategorySerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'course']



class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'



# class CartContentSerializer(serializers.ModelSerializer):
#     cart = serializers.StringRelatedField(read_only=True)
#     course = serializers.StringRelatedField(read_only=True)
#     class Meta:
#         model = CartContent
#         fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)
    class Meta:
        model = Cart
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(read_only=True)
    amount = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


    # def get_amount(self):
    #     pass




class EnrollSerializer(serializers.Serializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enroll
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'



class LikeSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = ReviewLike
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Favourite
        fields = '__all__'

