from xml.dom import ValidationErr
from rest_framework import serializers
from accounts.models import User, UserProfile
## importing for email password change
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import Util
import os

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style = {'input_type':'password'},write_only = True)

    class Meta:
        model = User
        fields = ['email','password','password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match!')
        return attrs
        
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(source='user.email')
    name = serializers.CharField(max_length=255,allow_null=True)
    phone = serializers.DecimalField(max_digits=10, decimal_places=0, allow_null=True)
    location = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'name','phone', 'location']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    
    phone = serializers.DecimalField(max_digits=10, decimal_places=0, allow_null=True)
    location = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['phone', 'location']

class UserProfileUpdateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name']




class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {'input': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length = 255, style = {'input': 'password'}, write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            print("password and confirm password not equal")
            return serializers.ValidationError("password and confirm password does not match")
        
        user.set_password(password)
        user.save()

        return attrs
    
class UserSendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            # sending mail for password reset
            user = User.objects.get(email=email)
            # urlsafe_base64_encode does not take integer but bytes
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://127.0.0.1:8000/api/user/reset/'+uid+'/'+token
            print('Password reset link', link)
            print (os.environ.get("EMAIL_USER")) 
            # Send mail
            body = 'Click following link to reset your password'+link
            data = {
                'subject' : 'Reset your password',
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise ValidationErr('You are not a registered user')
    
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style = {'input_type': 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type': 'password'},write_only=True)

    class Meta:
        fields = ['password','password2']

    # validate function custom
    def validate(self, attrs):
        # Try catch block to tackle token manipulation.
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            # We dont have user thats why we get the user from view itself.
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password dosent match")
            id = smart_str(urlsafe_base64_decode(uid))
            # finding the user with this id
            user = User.objects.get(id=id)
            # Validating correct token
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('token is not valid or expired')
            user.set_password(password) 
            user.save()

            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('token is not valid or manipulated')
        

