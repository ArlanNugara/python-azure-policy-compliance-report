import sys
import os
import json
import requests
from modules.get_policy import policyStatus

print("Starting Login Process")

# Login and get access token
try:
    LOGIN_URL = "https://login.microsoftonline.com/"+os.environ.get('ARM_TENANT_ID')+"/oauth2/token"
    PARAMS_MGMT = {'grant_type':'client_credentials','client_id': ''+os.environ.get('ARM_CLIENT_ID')+'','client_secret':''+os.environ.get('ARM_CLIENT_SECRET')+'','resource':'https://management.azure.com/'}
    login = requests.post(url = LOGIN_URL, data = PARAMS_MGMT)
    jsonfy = login.json()
    token = jsonfy["access_token"]
    query_header = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
    print("Login Successful")
except Exception as e:
    print("Error is ", e)
    print("Login Unsuccessful, please check your credentials")
    sys.exit(1)

# Get Policy Summary
try:
    policyStatus(sys.argv[1], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)