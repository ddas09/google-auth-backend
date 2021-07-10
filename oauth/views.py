from google.oauth2 import id_token
from google.auth.transport import requests
from django.http.response import JsonResponse
from .queries import userExists, registerUser
import json


# Google Client Id
CLIENT_ID = '68487148874-i4mps86crd2rn4fiualrcj8ticp8j4f4.apps.googleusercontent.com'


def verifyGoogleToken(idToken):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idInfo = id_token.verify_oauth2_token(idToken, requests.Request(), CLIENT_ID)
        
        # ID token is valid. Get the user's details
        user = {}
        user["id"] = idInfo["sub"]
        user["email"] = idInfo["email"]
        user["firstName"] = idInfo["given_name"]
        user["lastName"] = idInfo["family_name"]
        user["photoUrl"] = idInfo["picture"]
        return user
    except ValueError:
        # Invalid token
        return None


def login(request):
    if request.method == "POST":
        idToken = json.loads(request.body).get("idToken")
        if not idToken:
            response = {"message": "Missing id token in request", "errorCode": 603}
            return JsonResponse(response, status=403)   
        
        user = verifyGoogleToken(idToken)
        if not user: 
            response = {"message": "Invalid google id token", "errorCode": 601}
            return JsonResponse(response, status=401)

        if userExists(user["id"]):
            return JsonResponse(user) 
        else:
            response = {"message": "User account doesn't exist", "errorCode": 606}
            return JsonResponse(response, status=406)
        
    else:
        response = {"message": "Http method not allowed for this endpoint", "errorCode": 605}
        return JsonResponse(response, status=405)    


def register(request):
    if request.method == "POST":
        idToken = json.loads(request.body).get("idToken")
        if not idToken:
            response = {"message": "Missing id token in request", "errorCode": 603}
            return JsonResponse(response, status=403)   
        
        user = verifyGoogleToken(idToken)
        if not user: 
            response = {"message": "Invalid google id token", "errorCode": 601}
            return JsonResponse(response, status=401)

        if not userExists(user["id"]):
            registerUser(user)
            return JsonResponse(user) 
        else:
            response = {"message": "User account already exists", "errorCode": 606}
            return JsonResponse(response, status=406)
        
    else:
        response = {"message": "Http method not allowed for this endpoint", "errorCode": 605}
        return JsonResponse(response, status=405)      