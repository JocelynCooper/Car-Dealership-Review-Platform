from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from sqlalchemy import true
from .models import *
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf
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
    return redirect('django:index')


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
    if request.method == "GET":
        url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_by_id_from_cf(url, dealer_id)
        dealer_reviews = [[dealer.review, dealer.sentiment]
                          for dealer in reviews]
        return HttpResponse(dealer_reviews)


def add_review(request, dealer_id):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            content = request.POST

            review = {}
            if "purchase" in content:
                review["car_make"] = dealer_id
                review["car_model"] = dealer_id
                review["car_year"] = dealer_id
                review["purchase"] = True

            review["dealership"] = dealer_id
            review["id"] = -1
            review["name"] = user.username

            json_payload = {}
            json_payload["review"] = review

            url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/review"
            reviews = get_dealer_by_id_from_cf(url, dealer_id)
            dealer_reviews = [[dealer.review, dealer.sentiment]
                              for dealer in reviews]
            return HttpResponse(dealer_reviews)
