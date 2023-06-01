import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, params=None, auth=None):
    print(params)
    print("GET from {} ".format(url))
    try:
        if auth:
            # Call get method of requests library with URL, parameters, and authentication
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=params, auth=auth)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=params)
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
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        print("Network exception occurred")
        return None
    


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

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    params = {"dealerId": dealer_id}
    print("The dealer id chosen is:", dealer_id)
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        json_result = json.loads(response.text)
        for item in json_result:
            dealer_obj = DealerReview(
                dealership=item.get("dealership"),
                name=item.get("name"),
                purchase=item.get("purchase"),
                review=item.get("review"),
                purchase_date=item.get("purchase_date"),
                car_make=item.get("car_make"),
                car_model=item.get("car_model"),
                car_year=item.get("car_year"),
                sentiment=None,
                id=item.get("id")
            )
            dealer_obj.sentiment=analyze_review_sentiments(dealer_obj.review)
            print("The sentiment is: " + str(analyze_review_sentiments(dealer_obj.review)))
            results.append(dealer_obj)
    
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review_text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com"
    api_key = "TGUaus6MkkIJcYB33p0SgedRDG4Mg9eSGH7k59zltxim"
    
    if api_key:
        # Authentication parameters
        auth = HTTPBasicAuth('apikey', api_key)
        
        # NLU parameters
        params = {
            "text": review_text,
            "version": "2021-09-01",
            "features": "sentiment",
            "return_analyzed_text": True
        }
        
        # Make a request to analyze the sentiment of the review
        response = get_request(url, params=params, auth=auth)
        
        if response:
            sentiment = response.get("sentiment", {}).get("document", {}).get("label")
            return sentiment
    
    return None



