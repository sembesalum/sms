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
                SMSMessage.objects.create(
                    sender=sms.get('sender'),
                    receiver=sms.get('receiver'),
                    body=sms.get('body'),
                    timestamp=sms.get('timestamp'),
                    message_type=sms.get('type'),
                    delivery=sms.get('delivery'),
                    read=sms.get('read'),
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