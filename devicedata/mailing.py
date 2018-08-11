from django.core.mail import EmailMessage

class Mailing:

	def send_warning_mail(cause):
		subject = ' Warning from sensor service'
		body = 'This message was send because sensor station ' + cause + '\n exceeded safe limits\n' + 'Instant action recommended'
		admin = 'lauri.v.westerholm@gmail.com'
		email = EmailMessage(subject,body, to=[admin])
		email.send()