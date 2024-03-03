# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import CustomUser
from .serializers import CustomUserSerializer,UserProfileUpdateSerializer,UserProfileRetrieveSerializer
import random
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            password = make_password(serializer.validated_data.get('password'))
            serializer.validated_data['password'] = password
            user = serializer.save()
            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# link_manager/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Link
from .serializers import LinkSerializer
from django.shortcuts import get_object_or_404
class LinkViewSet(viewsets.ViewSet):


    def create(self, request):
        user_id = request.data.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user_id = request.query_params.get('user_id')
        if user_id is not None:
            queryset = Link.objects.filter(user_id=user_id)
        else:
            queryset = Link.objects.all()
        serializer = LinkSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request):
        link_id = request.query_params.get('id')
        if not link_id:
            return Response({'error': 'Link ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        link = get_object_or_404(Link, pk=link_id)
        link.delete()
        return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)

import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Link
from urllib.parse import urlencode

def generate_qr_codes(request):
    user_id = request.GET.get('user_id')
    if user_id is None:
        return HttpResponse("user_id parameter is required", status=400)

    links = Link.objects.filter(user_id=user_id)

    # Construct the query string for the URL
    query_string = urlencode({'user_id': user_id})

    qr_codes = BytesIO()

    for link in links:
        qr_data = f"{request.build_absolute_uri('/links/')}?{query_string}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_codes, format='PNG')

    qr_codes.seek(0)
    return HttpResponse(qr_codes.read(), content_type='image/png')
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from io import BytesIO
import qrcode
from .models import Link


def get_links_by_user_id(request):
    user_id = request.GET.get('user_id')
    if user_id is None:
        return JsonResponse({'error': 'user_id parameter is required'}, status=400)

    links = Link.objects.filter(user_id=user_id).values('id', 'url')
    return JsonResponse({'links': list(links)})

def qr_code_page(request):
    # Get the user_id from query parameters
    user_id = request.GET.get('user_id')
    if user_id is None:
        return HttpResponse("user_id parameter is required", status=400)

    # Construct the URL for the QR code
    query_string = urlencode({'user_id': user_id})
    qr_code_url = request.build_absolute_uri(reverse('generate-qr-codes') + f'?{query_string}')

    return render(request, 'qr_code_page.html', {'qr_code_url': qr_code_url})

@api_view(['GET'])
def user_profile_retrieve(request):
    user_id = request.GET.get('user_id')
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = UserProfileRetrieveSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def user_profile_update(request):
    user_id = request.data.get('user_id')
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
