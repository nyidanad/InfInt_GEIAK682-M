import socket
import time
import uuid
import json
import sqlite3
import datetime

HOST = '127.0.0.1'
PORT = 65432

# read .json file
with open('details.json', 'r') as file:
  details = json.load(file)


# create database table
db_conn = sqlite3.connect('transactions.db')
db_cursor = db_conn.cursor()
# db_cursor.execute('DROP TABLE Transactions')
db_cursor.execute("""
                  CREATE TABLE IF NOT EXISTS Transactions (
                    tid int PRIMARY KEY,
                    phoneNo varchar(20),
                    amount int,
                    date DATE
                  )
                  """)


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
          tid, phoneNo, amount = parts[1], parts[2], parts[3]
          date = datetime.datetime.now()
          date_time = date.strftime("%Y/%m/%d, %H:%M:%S")

          db_cursor.execute('INSERT INTO Transactions VALUES(?, ?, ?, ?)', (tid, phoneNo, amount, date_time))
          db_conn.commit()
          conn.send('UPLOADED'.encode())
          print('[S] >>> status: UPLOADED')

        elif parts[0] == 'LIST':
          db_cursor.execute('SELECT * FROM Transactions')
          rows = db_cursor.fetchall()
          res = '\n'.join([f"{r[0]} | {r[3]} | {r[1]} | {r[2]} Ft" for r in rows]) or "No data(s)"
          conn.send(res.encode())
          print('[S] >>> status: LISTED')

        else:
          conn.send('INVALID'.encode())
          print('[S] >>> status: INVALID')