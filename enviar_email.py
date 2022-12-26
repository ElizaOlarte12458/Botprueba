import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def CorreoDesprendible(correos): # enviar correo con el desprendible de nomina
	print("manda correo")
	print(correos)
	
	email_user = 'elizabetholarte0@gmail.com'
	email_send = correos
	subject = 'Prueba Chatbot'

	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject

	body = 'Hola, \n\nSoy PromiBot y me complace enviarte la información que solicitaste.'
	msg.attach(MIMEText(body,'plain'))

	filename = 'Promigas.pdf'
	attachment = open(filename,'rb')
	part = MIMEBase('application','octet-stream')
	part.set_payload ((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment'; filename = "+ filename )

	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com: 587')
	server.starttls()
	server.login(email_user,'kfcbzcavlfezxfwt')
	server.sendmail(email_user, email_send, text)
	server.quit()
	print("correo enviado")


# def CorreoLaboral(correos):  # enviar correo con el certificado laboral
# 	email_user = 'jamesbot@periferiaitgroup.com'
# 	email_send = correos
# 	subject = 'Certificado laboral'

# 	msg = MIMEMultipart()
# 	msg['From'] = email_user
# 	msg['To'] = email_send
# 	msg['Subject'] = subject

# 	body = 'Hola, \n\nSoy James Bot y me complace enviarte la información que solicitaste, descarga tu Certificado laboral.'
# 	msg.attach(MIMEText(body,'plain'))

# 	filename = 'Certificacion_laboral.pdf'
# 	attachment = open(filename,'rb')
# 	part = MIMEBase('application','octet-stream')
# 	part.set_payload ((attachment).read())
# 	encoders.encode_base64(part)
# 	part.add_header('Content-Disposition',"attachment'; filename = "+ filename )

# 	msg.attach(part)
# 	text = msg.as_string()
# 	server = smtplib.SMTP('smtp.office365.com',587)
# 	server.starttls()
# 	server.login(email_user,'Periferia2021/')
# 	server.sendmail(email_user, email_send, text)
# 	server.quit()

