from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SMSMessage
from django.core import serializers

@csrf_exempt
def sms_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sms_list = data.get('sms', [])

            for sms in sms_list:
                sender = sms.get('sender')
                receiver = sms.get('receiver')  # Ensure receiver exists
                body = sms.get('body')
                timestamp_value = sms.get('timestamp')

                # Validate required fields
                if not sender or not receiver:
                    return JsonResponse({'status': 'error', 'message': 'Sender and receiver are required'}, status=400)

                # Ensure timestamp is valid
                if timestamp_value:
                    if isinstance(timestamp_value, int):  # UNIX timestamp (milliseconds or seconds)
                        if timestamp_value > 9999999999:  # Convert milliseconds to seconds
                            timestamp_value = timestamp_value / 1000
                        timestamp = datetime.fromtimestamp(timestamp_value)
                    elif isinstance(timestamp_value, str):  # ISO formatted string
                        try:
                            timestamp = datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%S")
                        except ValueError:
                            return JsonResponse({'status': 'error', 'message': 'Invalid timestamp format. Expected YYYY-MM-DDTHH:MM:SS'}, status=400)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid timestamp format'}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Timestamp missing'}, status=400)

                # Save message to database
                SMSMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    body=body,
                    timestamp=timestamp,
                    message_type=sms.get('type', 'sms'),  # Default to 'sms' if missing
                    delivery=sms.get('delivery', ''),
                    read=sms.get('read', False),
                )

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def get_sms_data(request):
    sms_messages = SMSMessage.objects.all().order_by('-timestamp')
    sms_data = [
        {
            'id': sms.id,
            'sender': sms.sender,
            'receiver': sms.receiver,
            'body': sms.body,
            'timestamp': sms.timestamp,
            'type': sms.message_type,
            'delivery': sms.delivery,
            'read': sms.read,
        }
        for sms in sms_messages
    ]
    return JsonResponse({'sms_messages': sms_data}, safe=False)