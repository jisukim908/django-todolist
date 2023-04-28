from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        name = user.name
        gender = user.gender
        age = user.age
        introduction = user.introduction
        user.save()
        return user
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "age", "introduction")
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age
        return token