import optparse, sys, socket, json
 
class Server:
    def __init__(self, port):
        self.host = '127.0.0.1'
        self.port = port

    def listen(self):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.bind((self.host,self.port))
        listener.listen(0)
        print("[+] Waiting for Incoming Connection")
        self.connection,address = listener.accept()
        print("[+] Got a Connection from " + str(address))

    def send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive(self):
    	json_data = ""
    	while True:
    		try:
    			json_data = json_data + self.connection.recv(1024).decode()
    			return json.loads(json_data)
    		except ValueError:
    			continue

    def run(self):
    	self.listen()
    	received_data = self.receive()
    	if (received_data[0] == 'encode_decode'):
    		result = self.encode_text(received_data[1], received_data[2])
    	if (received_data[0] == 'change_text'):
    		result = self.change_text(received_data[1], received_data[2])
    	
    	self.send(result)

    def encode_text(self, text, key):
    	encoded_text = ""
    	for i in range(len(text)):
    		ch = text[i]
    		k = key[i%len(key)]
    		encoded_text += chr(ord(ch) ^ ord(k))
    	return encoded_text

    def change_text(self, text, dict_string):
    	words = text.split()
    	final_dict = eval(dict_string)
    	print(words)
    	for word in words:
    		if word in final_dict.keys():
    			text = text.replace(word, final_dict[word])
    	return text

class Client:
	def __init__(self, mode):
		self.mode = mode

	def connect(self, host, port):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((host, port))

	def send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

	def receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024).decode()
				return json.loads(json_data)
			except ValueError:
				continue

	def send_to_process(self, msg_file, aux_file):
		msg_text = open(msg_file, 'r').read()
		aux_text = open(aux_file, 'r').read()
		data = []
		data.append(self.mode)
		data.append(msg_text)
		data.append(aux_text)
		self.send(data)
		received_data = self.receive()
		print(received_data)



def main():
	parser = optparse.OptionParser()
	parser.add_option("-p", metavar="PORT", type= int, help="Port on which server listens")
	if sys.argv[1] == "client":
		parser.add_option("--host", dest = "host", help="Ip address of server")
		parser.add_option("--mode", dest = "mode", help="Mode which idetifies how program shoud operate")
		parser.add_option("--msg_file", dest = "msg_file", help="Path of the file which contains message")
		parser.add_option("--aux_file", dest = "aux_file", help="Key or json file according to mode")
	(options,arguments) = parser.parse_args()
	if sys.argv[1] == "client":
		client = Client(options.mode)
		client.connect(options.host, options.p)
		client.send_to_process(options.msg_file, options.aux_file)
	else:
		server = Server(options.p)
		server.run()

if __name__== "__main__":
	main()