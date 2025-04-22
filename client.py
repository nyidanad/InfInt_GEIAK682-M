import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  print('[C] Connected to the server')

  msg = 'Hello Server'.encode()
  s.sendall(msg)
  print('[C] Message sent to the server')

  data = s.recv(1024)
  print('[C] Acknowledge recieved from the server')

print(f'[C] Recieved data: {data.decode()}')