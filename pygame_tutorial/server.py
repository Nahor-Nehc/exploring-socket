import socket
from _thread import *
import sys

server = "192.168.0.21" # local address!!!!!
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.bind((server, port))
except socket.error as e:
  print(e)

s.listen(2)  # how many things it is going to allow to connect
print("Server started, waiting for connection")

pos = [(0, 0), (100, 100)]

def decode_pos(str_):
  str_ = str_.split(",")
  return int(str_[0]), int(str_[1])

def encode_pos(position):
  return str(position[0]) + "," + str(position[1])

def threaded_client(conn, current_player):
  conn.send(str.encode(encode_pos(pos[current_player])))
  reply = ""
  while True:
    try:
      data = conn.recv(2048) # receives the data
      data = data.decode("utf-8") # decode data, arg is the number of bits to receive
      data = decode_pos(data) # convert string to tuple of positions
      pos[current_player] = data

      
      if not data:
        print("disconnected")
        break
      
      else:
        if current_player == 1:
          reply = pos[0]
        elif current_player == 0:
          reply = pos[1]

        # print("Received:", data)
        # print("sending:", reply)
      
      conn.sendall(str.encode(encode_pos(reply))) # encodes with utf-8
    
    except:
      print("error")
      
  
  print("lost connection")
  conn.close()

current_player = 0
while True:
  conn, addr = s.accept() # accepts incoming connections, address = ip address
  print("Connected to:", addr)
  
  start_new_thread(threaded_client, (conn, current_player)) # allows the program to continue to look for new connections while client program runs
  current_player += 1