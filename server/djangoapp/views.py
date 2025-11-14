from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .populate import initiate
from .models import CarMake, CarModel  # <-- Added for Car models

# Logger setup
logger = logging.getLogger(__name__)

# ===========================
# LOGIN VIEW
# ===========================
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            response = {"userName": username}

            if user is not None:
                login(request, user)
                response["status"] = "Authenticated"
            else:
                response["status"] = "Failed"

            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return JsonResponse({"error": "Login failed"}, status=500)

    return JsonResponse({"status": "Method not allowed"}, status=405)


# ===========================
# LOGOUT VIEW
# ===========================
@csrf_exempt
def logout_request(request):
    if request.method == "POST":
        try:
            logout(request)
            data = {"userName": "", "status": "Logged out"}
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return JsonResponse({"error": "Logout failed"}, status=500)

    return JsonResponse({"status": "Method not allowed"}, status=405)


# ===========================
# REGISTRATION VIEW
# ===========================
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            # Create new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Log in the newly created user
            login(request, user)

            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return JsonResponse({"error": "Registration failed"}, status=500)

    return JsonResponse({"status": "Method not allowed"}, status=405)


# ===========================
# GET CARS VIEW
# ===========================
def get_cars(request):
    """
    Returns a JSON list of all car models along with their makes.
    If no CarMake exists, populate the database using initiate().
    """
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# ===========================
# PLACEHOLDER VIEWS
# ===========================
# def get_dealerships(request):
#     ...

# def get_dealer_reviews(request, dealer_id):
#     ...

# def get_dealer_details(request, dealer_id):
#     ...

# def add_review(request):
#     ...
