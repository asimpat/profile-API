from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import requests
from decouple import config


USER_EMAIL = config('USER_EMAIL')
USER_NAME = config('USER_NAME')
USER_STACK = config('USER_STACK')

@api_view(['GET'])
def me(request):
    try:
        # Fetch cat fact from external API
        cat_response = requests.get(
            'https://catfact.ninja/fact',
            timeout=5 
        )

        if cat_response.status_code == 200:
            cat_fact = cat_response.json().get('fact', 'Cats are amazing!')
        else:
            cat_fact = 'Cats are mysterious creatures.'

    except requests.exceptions.RequestException as e:
        # Fallback if API fails
        cat_fact = 'Cats are wonderful pets.'

    # Get current UTC timestamp in ISO 8601 format
    current_timestamp = datetime.utcnow().strftime(
        '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    #response
    response_data = {
        "status": "success",
        "user": {
            "email": USER_EMAIL,
            "name": USER_NAME,         
            "stack": USER_STACK
        },
        "timestamp": current_timestamp,
        "fact": cat_fact
    }

    return Response(response_data, status=status.HTTP_200_OK)
