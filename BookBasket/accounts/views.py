from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer, UserSendPasswordResetEmailSerializer, UserProfileUpdateSerializer, UserProfileUpdateNameSerializer
from django.contrib.auth import authenticate ## used to authenticate email and password
from accounts.renderer import UserRenderer ## Custom renderer class in renderer.py
from rest_framework_simplejwt.tokens import RefreshToken ## directly copied to create manually custom tokens from website.
from rest_framework.permissions import IsAuthenticated ## for authentication of user.
from accounts.models import User,UserProfile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):

    renderer_classes = [UserRenderer] ## only this much needs to be defined to have custom renderer.

    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  ## Raise exception stops the and return  the exception directly.
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token,'msg':'Registration Success'},status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    renderer_classes = [UserRenderer]

    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token,'msg':'Login Success'},status = status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors' : ['Email or password is not valid']}},status = status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST )
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_user_profile(self, user):
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            # If UserProfile does not exist, create a new one
            return UserProfile.objects.create(user=user)

    def get(self, request, format=None):
        # Retrieve the user's profile or create a new one if it doesn't exist
        user_profile = self.get_user_profile(request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_user_profile(self, user):
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            # If UserProfile does not exist, create a new one
            return UserProfile.objects.create(user=user)

    def put(self, request, format=None):
        # Retrieve the user's profile or create a new one if it doesn't exist
        user_profile = self.get_user_profile(request.user)
        
        # Use a different serializer for update
        serializer = UserProfileUpdateSerializer(user_profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileUpdateNameView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_user_profile(self, user):
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            # If UserProfile does not exist, create a new one
            return UserProfile.objects.create(user=user)

    def put(self, request, format=None):
        # Retrieve the user's profile or create a new one if it doesn't exist
        user_profile = self.get_user_profile(request.user)
        
        # Use a different serializer for update
        serializer = UserProfileUpdateNameSerializer(user_profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed sucessfully'}, status=status.HTTP_200_OK)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    
class UserSendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, fomrat=None):
        serializer = UserSendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link send. Please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, uid, token,fomrat=None):
        serializer = UserPasswordResetSerializer(data = request.data, context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset sucessfully!'},status=status.HTTP_200_OK)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    





# Create your views here.
