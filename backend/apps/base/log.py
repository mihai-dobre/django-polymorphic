import logging
from celery.utils.log import get_task_logger

log_send_sms = logging.getLogger('send_sms')
log_send_voice = logging.getLogger('send_voice')
log_twilio_api = logging.getLogger('twilio_api')
log_call_back = logging.getLogger('call_back')
log_celery_task = get_task_logger('celery_log')
log_smsbox_api = logging.getLogger('smsbox_api')