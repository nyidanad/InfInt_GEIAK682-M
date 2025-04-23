import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  print('[R] Connected to the server')

  s.send('LIST'.encode())
  print(f'[R] >>> request: retrieve data(s) from database')

  data = s.recv(4096).decode()
  print(data)
