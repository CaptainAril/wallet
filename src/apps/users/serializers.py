from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authentication import authenticate

from utilities.password_validation import validate_password

from .models import User, UserKYCInformation, UserNextOfKin


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone']
    
    def create(self, validated_data):
        validate_password(validated_data['password'])
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email and not password:
            raise serializers.ValidationError(_('Eamil and Password required!'))

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(_('Incorrect Login Credentials!'))

        assert user.is_verified, _('Please verify your email first.')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNextOfKin
        fields = '__all__'

        
class UserKYCInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKYCInformation
        fields = '__all__'

class EmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attr):
        attr['email'] = attr['email'].lower()
        if not User.objects.filter(email=attr['email']).exists():
            raise serializers.ValidationError(_('User with this email does not exist.'))
        return User.objects.get(email=attr['email'])


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('token')
        uid = attrs.get('uid')

        if not token or not uid:
            raise serializers.ValidationError(_('Token and UID are required.'))

        return attrs