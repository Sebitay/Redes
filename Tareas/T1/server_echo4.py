#!/usr/bin/python3
# Echo server program - version of server_echo4_n.c
# Usando threads para multi-clientes
import os, signal
import sys, threading
import jsockets

class ClientThread(threading.Thread):
    def __init__(self, addr, s):
        threading.Thread.__init__(self)
        self.sock = s
    def run(self):
        print('Cliente Conectado', file=sys.stderr)
 
        while True:
            try:
                data = self.sock.recv(1024*1024)
                if not data: break
            except:
                print('socket exception', file=sys.stderr)
                return
            try:
                self.sock.send(data)
            except:
                print('socket exception', file=sys.stderr)
                return
        self.sock.close()
        print('Cliente desconectado', file=sys.stderr)

# Main
s = jsockets.socket_tcp_bind(1819)
if s is None:
    print('could not open socket', file=sys.stderr)
    sys.exit(1)
while True:
    conn, addr = s.accept()
    newthread = ClientThread(addr, conn)
    newthread.start()
