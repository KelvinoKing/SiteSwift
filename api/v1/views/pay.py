#!/usr/bin/python3
""" Module for pay view """

from api.v1.views import app_views
from flask import jsonify, abort, request
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime


my_endpoint = "https://8744-154-70-56-129.ngrok-free.app"

@app_views.route('/pay', methods=['POST'], strict_slashes=False)
def MpesaExpress():
  """Make a payment request to Safaricom API"""

  data = request.get_json()
  amount = data.get('amount')
  phone_number = data.get('phone_number')

  endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
  access_token = getAccessToken()
  headers = {"Authorization": "Bearer %s" % access_token}
  Timestamp = datetime.now()
  times = Timestamp.strftime("%Y%m%d%H%M%S")
  password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
  password = base64.b64encode(password.encode('utf-8'))

  data = {
    "BusinessShortCode": "174379",
    "Password": password,
    "Timestamp": times,
    "TransactionType": "CustomerPayBillOnline",
    "PartyA": phone_number,
    "PartyB": "174379",
    "PhoneNumber": phone_number,
    "CallBackURL": "https://8744-154-70-56-129.ngrok-free.app/api/v1/callback",
    "AccountReference": "Test",
    "TransactionDesc": "Test",
    "Amount": amount
  }

  # Assuming `data` is a dictionary that might contain bytes objects
  for key, value in data.items():
     if isinstance(value, bytes):
       data[key] = value.decode()  # decode bytes to string
  response = requests.post(endpoint, json=data, headers=headers)
  return jsonify(response.json())


@app_views.route('/callback', methods=['POST'])
def incoming():
    data = request.json
    print(data)
    return "OK"


"""Get access token from Safaricom API
"""
def getAccessToken():
    consumer_key = "9dQuqUZwvCAY5Pa18FTgaTKmullyoqE51NSVFea9od7of0s3"
    consumer_secret = "ASfmOs5tzL47rJi3a1dBZH0c3jXR8IkirxaZQhrEEfG3wVD9gApkfGb5ba6GgcG3"
    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = response.json()
    return data["access_token"]
