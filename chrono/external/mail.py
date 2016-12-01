import poplib
host = "202.141.80.13"
port = 995
email = "k.raghuram"
pwd = "totallymypassword"

server = poplib.POP3_SSL(host, port)
try: 
	server.user(email)
	if('+OK'):
		server.pass_(pwd)
		if("+OK Logged in."):
			numMessages = len(server.list()[1])
			for i in range(100):
				text = '\n'.join(server.retr(i+1)[1])
				text.decode
				print "Mail No : "+str(i+1)
				print text
			server.quit()
except poplib.error_proto:
	print "u are fucked"
