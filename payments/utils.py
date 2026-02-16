import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import datetime
import base64

def format_phone_number(phone):
    phone = phone.strip()
    if phone.startswith('0'):
        return '254' + phone[1:]
    elif phone.startswith('254'):
        return phone
    elif phone.startswith('+254'):
        return phone[1:]
    return phone

def get_access_token():
    res = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    )
    return res.json().get('access_token')

def initiate_stk_push(phone, amount, booking_id):
    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()
    
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": format_phone_number(phone),
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": format_phone_number(phone),
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"BookID{booking_id}",
        "TransactionDesc": "Car Rental Payment"
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)
    return response.json()