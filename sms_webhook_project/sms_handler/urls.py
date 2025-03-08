from django.urls import path
from . import views

urlpatterns = [
    path('sms-webhook/', views.sms_webhook, name='sms_webhook'),
    path('sms-data/', views.get_sms_data, name='get_sms_data'),
]