from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import MyUser
from account.send_mail import send_confirmation_email
from main.models import User


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('пароли не совпадают')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_confirmation_email(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(requests=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'пользователь не может залогинется с передоставлеными  данными'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = "вы не заполнили имэил или пароль"
            raise serializers.ValidationError(message, code='authenticate')

        attrs['user'] = user
        return attrs


