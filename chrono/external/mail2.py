import poplib
from email.parser import Parser
host = "202.141.80.13"
port = 995
email = "k.raghuram"
pwd = "totallymypassword"
server = poplib.POP3_SSL(host, port)
server.user(email)
server.pass_(pwd)
server.stat()
for i in [3,5,14,20,23,25,49,50,51,52,61,64,84,85,86]:#range(100):
	text = '\n'.join(server.retr(i)[1])
	message = Parser().parsestr(text)
	# print message['from']
	# print message['to']
	# print message['date']
	# print message['subject']
	print "Mail Number : "+str(i)
	print text
		# print message.get_charset()
		# if message.get_charset() is None:
		# 	try:
		# 		print [i.get_charset() for i in message.get_payload()]
		# 	except Exception as e:
		# 		print e
	body = []
	if(message.get_content_type()=='text/plain'):
		body.append(message.get_payload())
	elif(message.get_content_type()=='multipart/mixed'):
		payload = message.get_payload()
		for i in payload:
			if(i.get_content_type()=='text/plain'):
				body.append(i.get_payload())
	body = '\n'.join(body)
	# print body
