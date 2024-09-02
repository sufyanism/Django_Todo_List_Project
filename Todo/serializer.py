from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields = "__all__"


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    username = serializers.EmailField(max_length=150, ),
    # first_name = serializers.CharField(max_length=150, )
    email=serializers.EmailField(max_length= 100,)
    password = serializers.CharField(max_length=65, write_only=True)

        
    class Meta:
        model = User
        fields = ['id','username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, attrs):
            email = attrs.get('email', '')
            if User.objects.filter(email=email).exists():
                 raise serializers.ValidationError(
                     {'email': ('Email is already in use')})
            return super().validate(attrs)

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['username'],
                validated_data['first_name'],
                validated_data['email'],
                )       
            user.set_password(validated_data['password'])
            user.save()
            return user 



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=150, ),
    password = serializers.CharField(max_length=65, write_only=True)


    def validate(self, data):
        user = authenticate(**data) # type: ignore
        if user and user.is_active:
            return user
        raise serializers.ValidationError({'Msg': ('Invalid your')})

    class Meta:
        model = User
        fields = ['username', 'password']