# Uncomment the required imports before adding the code
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
import requests

from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return (
                JsonResponse({"error": "Username already exists"}, status=400)
            )

        if User.objects.filter(email=email).exists():
            return (
                JsonResponse({"error": "Email already in use"}, status=400)
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        login(request, user)
        return JsonResponse(
            {"status": "success", "userName": username},
            status=201
        )

    return (
             JsonResponse({"error": "Invalid request method"}, status=405)
    )


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append(
            {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        )
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            print(response)
            review_detail["sentiment"] = response["sentiment"]
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return JsonResponse(
            {"status": 401, "message": "Request failed"},
            status=401
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON error: {e}")
        return JsonResponse(
            {"status": 401, "message": "Invalid JSON"},
            status=401
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse(
            {"status": 401, "message": "Unexpected server error"},
            status=401
        )
