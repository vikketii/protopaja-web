# Celery tasks, run as a daemon process

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
from .models import Device, Data, Email, Alarm

@shared_task
def send_warning_mail(user,cause):
	subject = ' Warning from Consair sensor system'
	body = 'This message was sent because ' + cause + '\n dust values exceeded safe limits.\n' + 'Instant action recommended!'
	
	email = EmailMessage(subject,body, to=[user])
	email.send()

@shared_task
def update_device_warnings(device_id, dust, time):
	# id is device id, int
	# dust is the latest dust value, compared to Device dust_set_point
	device = Device.objects.get(id=device_id) #this will fail if device isn't found
	if device:
		
		if dust >= device.dust_set_point:
			device.dust_warnings += 1
			device.save(update_fields=['dust_warnings'])
			if device.dust_warnings == device.dust_trigger:
				Alarm.objects.create(alarm_type=device.info+': too many dust particles!',time=time)
				return True
			else:
				return False


		else:
			# dust value was ok, so reset warnings
			device.dust_warnings = 0 
			return False





@shared_task
def warning_emails(device, device_id, dust, time):
	# device is device name
	
	# first update warnings to Device objects
	warnings = update_device_warnings(device_id, dust, time)


	if warnings:
		emails = Email.objects.all()

		for i in range(0,len(emails)):
		
			if emails[i].device_name == device or emails[i].device_name == 'All':
				send_warning_mail(emails[i].address, device) # if mails are send more, group mail should be used