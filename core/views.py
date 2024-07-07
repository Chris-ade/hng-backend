# core/views.py
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Organization
from .serializers import UserSerializer, OrganizationSerializer

API_KEY = '0b98a1cd77c455039947dd692915806e'

def index(request):
    return HttpResponse('Hello world.')

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR')

    # Fetch location information
    location_response = requests.get(f'https://ipinfo.io/{client_ip}/json')
    location_data = location_response.json()
    city = location_data.get('city', 'Unknown location')
    
    # Fetch weather information
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}')
    weather_data = weather_response.json()
    
    print(weather_data)
    
    if (weather_data.get('cod') == 401 or weather_data.get('cod') == 404):
        return JsonResponse({'message': weather_data.get('message')})
    else:
        temperature = weather_data['main']['temp']
        response = {
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
        }
        return JsonResponse(response)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            save_data = user.save()
            
            if save_data is False:
                return Response({
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400
                }, status=status.HTTP_400_BAD_REQUEST)

            org_name = f"{user.firstName}'s Organisation"
            org_desc = f"{user.firstName}'s organisation description"
            org = Organization.objects.create(orgId=user.userId, name=org_name, description=org_desc)
            org.users.add(user)
            org.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        return Response({
            "errors": [
                {"field": field, "message": str(message[0])}
                for field, message in errors.items()
            ]
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.filter(userId=id).first()
        if user and (user == request.user or user in request.user.organizations.all().users):
            return Response({
                "status": "success",
                "message": "User details fetched successfully",
                "data": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "User not found or access denied",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)

class UserOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organisations = request.user.organizations.all()
        return Response({
            "status": "success",
            "message": "Organisations fetched successfully",
            "data": {
                "organisations": OrganizationSerializer(organisations, many=True).data
            }
        }, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            organization.users.add(request.user)
            organization.save()

            return Response({
                "status": "success",
                "message": "Organisation created successfully",
                "data": OrganizationSerializer(organization).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "errors": [
                {"field": field, "message": str(message[0])}
                for field, message in serializer.errors.items()
            ]
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class SingleOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orgId):
        organization = Organization.objects.filter(orgId=orgId).first()
        if organization and request.user in organization.users.all():
            return Response({
                "status": "success",
                "message": "Organisation details fetched successfully",
                "data": OrganizationSerializer(organization).data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Organization not found or access denied",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUserToOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId):
        userId = request.data.get('userId')
        organization = Organization.objects.filter(orgId=orgId).first()
        user = User.objects.filter(userId=userId).first()

        if not organization or not user:
            return Response({
                "status": "Bad request",
                "message": "Organization or User not found",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        organization.users.add(user)
        organization.save()

        return Response({
            "status": "success",
            "message": "User added to organization successfully",
        }, status=status.HTTP_200_OK)