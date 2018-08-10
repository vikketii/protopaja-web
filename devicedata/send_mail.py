from django.core.mail import EmailMessage


def send_warning_mail(cause):
	subject = ' Warning from sensor service'
	body = 'This message was send because ' + cause + '\n exceeded safe limits\n' + 'Instant action recommended'
	admin = 'lauri.v.westerholm@gmail.com'
	email = EmailMessage(subject,body, to=[admin])
	email.send()