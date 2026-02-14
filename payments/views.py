import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import MpesaTransaction

from .utils import initiate_stk_push

@login_required
def process_payment(request, booking_id):
    from bookings.models import Booking
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = booking.total_price
        
        response = initiate_stk_push(phone, amount, booking.id)
        
        if response.get('ResponseCode') == '0':
            MpesaTransaction.objects.create(
                booking=booking,
                phone_number=phone,
                checkout_request_id=response.get('CheckoutRequestID'),
                amount=amount
            )
            return render(request, 'payments/waiting.html', {'checkout_id': response.get('CheckoutRequestID')})
        
    return render(request, 'payments/pay.html', {'booking': booking})

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    stk_callback = data['Body']['stkCallback']
    result_code = stk_callback['ResultCode']
    checkout_id = stk_callback['CheckoutRequestID']

    transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_id)

    if result_code == 0:
        transaction.status = 'Completed'
        # Extract Receipt Number from Metadata
        items = stk_callback['CallbackMetadata']['Item']
        for item in items:
            if item['Name'] == 'MpesaReceiptNumber':
                transaction.receipt_number = item['Value']
        
        transaction.save()
        
        # Update Booking & Car Availability
        booking = transaction.booking
        booking.status = 'confirmed'
        booking.save()
        
        car = booking.car
        car.is_available = False
        car.save()
    else:
        transaction.status = 'Failed'
        transaction.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})

def check_payment_status(request, checkout_id):
    transaction = get_object_or_404(MpesaTransaction, checkout_request_id=checkout_id)
    return JsonResponse({'status': transaction.status})