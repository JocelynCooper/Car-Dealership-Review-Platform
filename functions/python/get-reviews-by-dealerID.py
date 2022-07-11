from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = ""
url = ""
database = "reviews"


def format(response):
    response = response["docs"]
    formatted_response = []
    for res in response:
        del res["_id"]
        del res["_rev"]
        formatted_response.append(res)
    result = {"review": formatted_response}
    return result


def main(dict):
    authenticator = IAMAuthenticator(apikey=apikey)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(url)
    try:
        response = client.post_find(
            db=database,
            selector={'dealership': {'$eq': int(dict["id"])}},
        ).get_result()
        try:
            return format(response)
        except:
            return {
                'statusCode': 500,
                'message': 'Something went wrong on the server'
            }
    except:
        return {
            'statusCode': 404,
            'message': 'Database or dealerId does not exist'
        }


if __name__ == "__main__":
    dict = {"id": 15}
    main(dict)
