import re
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = ""
url = ""
database = "reviews"


def main(review):
    authenticator = IAMAuthenticator(apikey=apikey)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(url)
    try:
        response = client.post_document(
            db=database, document=review["review"]).get_result()
        return response
    except:
        return {
            'statusCode': 404,
            'message': 'Database or dealerId does not exist'
        }


if __name__ == "__main__":
    review = {
        "review":
        {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
    }
    main(review=review)
