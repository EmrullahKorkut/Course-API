from rest_framework import serializers

from courses.models import User


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
    
