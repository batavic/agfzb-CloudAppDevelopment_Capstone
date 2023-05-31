import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
        return None


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    response = requests.get(url, **kwargs)
    if response.status_code == 200:
        json_result = json.loads(response.text)
        for item in json_result:
            dealer_doc = item.get("doc")
            if dealer_doc:
                dealer_obj = CarDealer(
                    address=dealer_doc.get("address"),
                    city=dealer_doc.get("city"),
                    full_name=dealer_doc.get("full_name"),
                    id=dealer_doc.get("id"),
                    lat=dealer_doc.get("lat"),
                    long=dealer_doc.get("long"),
                    short_name=dealer_doc.get("short_name"),
                    st=dealer_doc.get("st"),
                    zip=dealer_doc.get("zip")
                )
                results.append(dealer_obj)
    return results
    
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



