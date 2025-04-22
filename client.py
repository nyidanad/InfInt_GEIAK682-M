import socket
import random
import json

HOST = '127.0.0.1'
PORT = 65432

# read .json file
with open('details.json', 'r') as file:
  details = json.load(file)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  print('[C] Connected to the server')

  phoneNo = random.choice(details['phoneNumbers'])
  amount = random.choice(details['amounts'])
  s.send(f'REQ,{phoneNo},{amount}'.encode())
  print(f'[C] >>> request: {phoneNo} <-- {amount} Ft')

  ack = s.recv(1024).decode().split(',')
  if ack[0] == 'OK':
    tid = ack[1]
    s.send(f'CONF,{tid},{phoneNo},{amount}'.encode())
    print(f'[S] >>> status: {s.recv(1024).decode()}')

  elif ack[0] == 'ERR':
    print('[S] >>> status: ERROR')