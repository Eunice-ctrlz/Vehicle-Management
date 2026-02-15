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
    from django.contrib import messages
    import logging
    logger = logging.getLogger('payments')

    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = booking.total_price
        
        try:
            response = initiate_stk_push(phone, amount, booking.id)
            logger.info(f"STK push response: {response}")
        except Exception as e:
            logger.error(f"STK push error: {e}")
            messages.error(request, f"Payment error: {str(e)}")
            return render(request, 'payments/pay.html', {'booking': booking})
        
        response_code = response.get('ResponseCode')
        if str(response_code) == '0':
            MpesaTransaction.objects.create(
                booking=booking,
                phone_number=phone,
                checkout_request_id=response.get('CheckoutRequestID'),
                amount=amount
            )
            checkout_id = response.get('CheckoutRequestID')
            logger.info(f"Transaction created: {checkout_id}")
            return render(request, 'payments/waiting.html', {'checkout_id': checkout_id})
        else:
            error_msg = response.get('errorMessage', 'Unknown error')
            logger.warning(f"Payment failed: {error_msg}")
            messages.error(request, f"Payment failed: {error_msg}")
        
    return render(request, 'payments/pay.html', {'booking': booking})

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    stk_callback = data['Body']['stkCallback']
    result_code = stk_callback['ResultCode']
    checkout_id = stk_callback['CheckoutRequestID']

    transaction = MpesaTransaction.objects.filter(checkout_request_id=checkout_id).first()

    if not transaction:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Transaction not found"})

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
        transaction.status = 'Cancelled' if result_code == 1032 else 'Failed'
        transaction.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})

def check_payment_status(request, checkout_id):
    transaction = get_object_or_404(MpesaTransaction, checkout_request_id=checkout_id)
    return JsonResponse({'status': transaction.status})

