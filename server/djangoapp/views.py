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
from .restapis import get_request, analyze_review_sentiments, post_review  # <-- Include post_review

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
# DEALER VIEWS
# ===========================
def get_dealerships(request, state="All"):
    """
    Return list of dealerships.
    If state="All", returns all dealerships; else filters by state.
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    """
    Return details of a particular dealer by dealer_id.
    """
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    """
    Return reviews for a dealer with sentiment analysis.
    """
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ===========================
# ADD REVIEW VIEW
# ===========================
@csrf_exempt
def add_review(request):
    """
    Allows an authenticated user to post a review for a dealer.
    """
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            print("Post response:", response)
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception as e:
            logger.error(f"Error posting review: {str(e)}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
