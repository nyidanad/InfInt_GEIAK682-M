import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  print(f'[S] Server listening on: {HOST}:{PORT}')

  while True:
    conn, addr = s.accept()
    with conn:
      print(f'[S] Connected from {addr} address')

      while True:
        data = conn.recv(1024)
        if not data:
          break
        print(f'[S] address: {addr}')
        print(f'[S] data: {data.decode()}')
        res = "OK".encode()
        conn.sendall(res)