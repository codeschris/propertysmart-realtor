from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST

class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Token is valid if we reach this point
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)

@csrf_exempt  # Only use this for development; consider using proper CSRF protection in production
@require_POST
def register(request):
    import json
    data = json.loads(request.body)

    name = data.get('name')
    email_address = data.get('email_address')
    phone_number = data.get('phone_number')
    password = data.get('password')
    user_type = data.get('user_type')

    if not (name and email_address and phone_number and password and user_type):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if User.objects.filter(email_address=email_address).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)

    # Create and save the user
    user = User(
        name=name,
        email_address=email_address,
        phone_number=phone_number,
        password=make_password(password),  # Hash the password
        user_type=user_type
    )
    user.save()

    return JsonResponse({'message': 'Registration successful'}, status=201)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)