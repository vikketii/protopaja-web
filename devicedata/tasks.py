# Celery tasks, run as a daemon process
# This contains the heavy work, base of whole alarm system

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
from .models import Device, Data, Email, Alarm

@shared_task
def send_warning_mail(user,cause):
	subject = ' Warning from Consair sensor system'
	body = 'This message was sent because ' + cause + '\n' + 'exceeded set treshold(s).\n' + 'Instant action recommended!'
	
	email = EmailMessage(subject,body, to=[user])
	email.send()

@shared_task
def update_device_warnings(device_id, dust, time, temp, humd, light):
	# id is device id, int
	# dust is the latest dust value, compared to Device dust_set_point
	device = Device.objects.get(id=device_id) #this will fail if device isn't found
	warnings = [0,0,0,0] #dust, temp, humd, light, the order crusial, this is basically a list of booleans

	if device:
		
		
		if dust >= device.dust_set_point:
			device.dust_warnings += 1
			device.save(update_fields=['dust_warnings'])
			if device.dust_warnings == device.dust_trigger:
				Alarm.objects.create(alarm_type=device.info+': too many dust particles!',time=time, device_id=device_id, alarm='dust')
				warnings[0] = 1

		else:
			# dust value was ok, so reset warnings
			device.dust_warnings = 0
			device.save(update_fields=['dust_warnings'])
			alarms = Alarm.objects.select_related().filter(device_id=device_id, time_over=None, alarm='dust')
			for i in range(0,len(alarms)):
				#add time over to all alarms which are triggered from this device
				alarms[i].time_over = time
				alarms[i].save(update_fields=['time_over'])

		if temp >= device.temp_treshold:
			device.temp_warnings += 1
			device.save(update_fields=['temp_warnings'])
			if device.temp_warnings == device.temp_trigger:
				Alarm.objects.create(alarm_type=device.info+': temperature too high!',time=time, device_id=device_id, alarm='temp')
				warnings[1] = 1

		else:
			device.temp_warnings = 0
			device.save(update_fields=['temp_warnings'])
			alarms = Alarm.objects.select_related().filter(device_id=device_id, time_over=None, alarm='temp')
			for i in range(0,len(alarms)):
				#add time over to all alarms which are triggered from this device
				alarms[i].time_over = time
				alarms[i].save(update_fields=['time_over'])

		if humd >= device.humd_treshold:
			device.humd_warnings += 1
			device.save(update_fields=['humd_warnings'])
			if device.humd_warnings == device.humd_trigger:
				Alarm.objects.create(alarm_type=device.info+': humidity too high!',time=time, device_id=device_id, alarm='humd')
				warnings[2] = 1

		else:
			device.humd_warnings = 0
			device.save(update_fields=['humd_warnings'])
			alarms = Alarm.objects.select_related().filter(device_id=device_id, time_over=None, alarm='humd')
			for i in range(0,len(alarms)):
				#add time over to all alarms which are triggered from this device
				alarms[i].time_over = time
				alarms[i].save(update_fields=['time_over'])


		if light >= device.light_treshold:
			device.light_warnings += 1
			device.save(update_fields=['light_warnings'])
			if device.light_warnings == device.light_trigger:
				Alarm.objects.create(alarm_type=device.info+': light value too high!',time=time, device_id=device_id, alarm='light')
				warnings[3] = 1

		else:
			device.light_warnings = 0
			device.save(update_fields=['light_warnings'])
			alarms = Alarm.objects.select_related().filter(device_id=device_id, time_over=None, alarm='light')
			for i in range(0,len(alarms)):
				#add time over to all alarms which are triggered from this device
				alarms[i].time_over = time
				alarms[i].save(update_fields=['time_over'])

	return warnings






@shared_task
def warning_emails(device, device_id, dust, time, temp, humd, light):
	# device is device name
	
	# first update warnings to Device objects
	warnings = update_device_warnings(device_id, dust, time, temp, humd, light)


	if warnings != [0,0,0,0]:
		emails = Email.objects.all()

		for i in range(0,len(emails)):
		
			if emails[i].device_name == device or emails[i].device_name == 'All':
				send_warning_mail(emails[i].address, device) # if mails are send more, group mail should be used