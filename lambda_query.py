import json
import requests

region = 'us-west-1'
service = 'es'
awsauth = ('user', 'password')

host = 'https://search-nutripair-dev2-toqicucpwv65awgbezwshuwbvy.us-west-1.es.amazonaws.com' # The OpenSearch domain endpoint with https://
index = 'usdafoods'
url = host + '/' + index + '/_search'

# Lambda execution starts here
def lambda_handler(event, context):

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    query = {
        "query": {
            "match": {
                "Food_Description": event['queryStringParameters']['q'],
            }
        }
    }

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response
