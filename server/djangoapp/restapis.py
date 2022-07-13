import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url,
                                 params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    print(kwargs)
    if "state" in kwargs:
        json_result = get_request(url, id=kwargs.get("state"))
    elif kwargs.get("dealer_id"):
        print(kwargs.get("dealer_id"))
        json_result = get_request(url, id=int(kwargs.get("dealer_id")))
    else:
        json_result = get_request(url)

    results = []
    if json_result:
        dealers = json_result["result"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url, id=dealerId)

    results = []
    if json_result:
        dealers = json_result["result"]
        for dealer_doc in dealers:
            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                      review=dealer_doc["review"], purchase_date=dealer_doc[
                                          "purchase_date"], car_make=dealer_doc["car_make"],
                                      car_model=dealer_doc["car_model"],
                                      car_year=dealer_doc["car_year"], id=dealer_doc["id"], sentiment="")
            dealer_obj.sentiment = analyze_review_sentiments(
                dealer_obj.review * 5)
            results.append(dealer_obj)

    return results


def analyze_review_sentiments(text):
    url = ""
    api_key = ""
    authenticator = IAMAuthenticator(api_key)
    nlp_server = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    nlp_server.set_service_url(url)
    response = nlp_server.analyze(text=text, features=Features(
        sentiment=SentimentOptions(targets=[text]))).get_result()
    sentiment = response['sentiment']['document']['label']
    print(sentiment)
    return sentiment
