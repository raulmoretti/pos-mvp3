from mailjet_rest import Client
import os

api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_SECRET_KEY")
mailjet = Client(auth=(api_key, api_secret), version='v3.1')