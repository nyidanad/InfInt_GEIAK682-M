import socket
import time
import uuid
import json

HOST = '127.0.0.1'
PORT = 65432

# read .json file
with open('details.json', 'r') as file:
  details = json.load(file)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  print(f'[S] Server listening on: {HOST}:{PORT}')

  while True:
    conn, addr = s.accept()
    with conn:
      print(f'[S] Connected from {addr} address')

      while True:
        data = conn.recv(1024).decode()
        if not data:
          break
        
        parts = data.split(',')
        time.sleep(1)
        if parts[0] == 'REQ':
          phoneNo = parts[1]
          amount = int(parts[2])
          print(f'[C] >>> phoneNo: {phoneNo}, amount: {amount}')

          if phoneNo not in details['phoneNumbers'] or amount not in details['amounts']:
            conn.send('ERR'.encode())
            print('[S] >>> status: ERROR')
            continue

          tid = str(uuid.uuid4())
          conn.send(f'OK,{tid}'.encode())
          print('[S] >>> status: OK')

        elif parts[0] == 'CONF':
          conn.send('UPLOADED'.encode())
          print('[S] >>> status: UPLOADED')

        else:
          conn.send('INVALID'.encode())
          print('[S] >>> status: INVALID')