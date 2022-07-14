from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from sqlalchemy import true
from .models import *
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_by_id_from_cf(url, dealer_id)
        context["reviews"] = reviews
        dealer_url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer_fullname = get_dealers_from_cf(dealer_url, dealer_id=dealer_id)[0].full_name
        context["dealer_fullname"] =  dealer_fullname
        context["dealer_id"] =  dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}
    dealer_url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/dealership"
    dealer_fullname = get_dealers_from_cf(dealer_url, dealer_id=dealer_id)[0].full_name
    context["dealer_fullname"] = dealer_fullname
    context["dealer_id"] = dealer_id
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)

            review = dict()
            if "purchase" in request.POST:
                review["purchase"] = True
                review["purchase_date"] = request.POST["purchasedate"]
            else:
                review["purchase"] = False
                review["purchase_date"] = "01/01/2000"

            review["dealership"] = dealer_id
            review["id"] = -1
            review["name"] = user.username
            review["review"] = request.POST["content"]
            review["car_make"] = car.carMakeName
            review["car_model"] = car.name
            review["car_year"] = int(car.year)

            json_payload = {}
            json_payload["review"] = review

            url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/review"
            post_request(url, json_payload)
        elif request.method == "GET":
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context["cars"] = cars
            return render(request, 'djangoapp/add_review.html', context)
    if request.method == "GET":
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context["cars"] = cars
            return render(request, 'djangoapp/add_review.html', context)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)