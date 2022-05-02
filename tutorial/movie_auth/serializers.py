from rest_framework import serializers
from .models import MyUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["username","password","email","dob",]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        dob = validated_data["dob"]

        user = MyUser.objects.create_user(username=username,password=password,
                                          email=email, dob=dob,)
        return user

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=250)

