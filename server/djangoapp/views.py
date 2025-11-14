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

# Logger setup
logger = logging.getLogger(__name__)


# ===========================
# LOGIN VIEW
# ===========================
@csrf_exempt
def login_user(request):
    """
    Handle POST login request.
    Returns JSON with username and authentication status.
    """
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
    """
    Handle POST logout request.
    Terminates the session and returns JSON with empty username.
    """
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
    """
    Handle POST registration request.
    Creates a new user, logs them in, and returns JSON with username and status.
    """
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

            # Return success JSON
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return JsonResponse({"error": "Registration failed"}, status=500)

    return JsonResponse({"status": "Method not allowed"}, status=405)


# ===========================
# PLACEHOLDER VIEWS
# ===========================
# Example placeholders you can implement later

# Get dealerships
# def get_dealerships(request):
#     ...

# Get dealer reviews
# def get_dealer_reviews(request, dealer_id):
#     ...

# Get dealer details
# def get_dealer_details(request, dealer_id):
#     ...

# Add review
# def add_review(request):
#     ...
