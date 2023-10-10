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


def threaded_client(conn):
  conn.send(str.encode("Connected"))
  reply = ""
  while True:
    try:
      data = conn.recv(2048) # receives data, arg is the number of bits to receive
      reply = data.decode("utf-8") # decodes sent data
      
      if not data:
        print("disconnected")
        break
      
      else:
        print("Received:", reply)
        print("sending:", reply)
      
      conn.sendall(str.encode(reply)) # encodes with utf-8
    
    except:
      break
  
  print("lost connection")
  conn.close()


while True:
  conn, addr = s.accept() # accpets incoming connections, address = ip address
  print("Connected to:", addr)
  
  start_new_thread(threaded_client, (conn,)) # allows the program to continue to look for new connections while client program runs