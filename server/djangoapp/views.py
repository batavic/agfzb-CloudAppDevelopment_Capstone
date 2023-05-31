from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarModel
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
    
# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'djangoapp/index.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('/')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('djangoapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/d714be82-5315-4975-bb14-898b8ff9635e/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/d714be82-5315-4975-bb14-898b8ff9635e/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        # Analyze sentiment for each review
        for review in reviews:
            review.sentiment = analyze_review_sentiments(review.review)
        
        # Prepare the response string with reviews and sentiment
        response = ''
        for review in reviews:
            response += f"Review: {review.review}<br>"
            response += f"Sentiment: {review.sentiment}<br><br>"
        
        return HttpResponse(response)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

