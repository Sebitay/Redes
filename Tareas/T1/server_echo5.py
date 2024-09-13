#!/usr/bin/python3
# Echo server program 
# Usando select para multi-clientes, version simple: bad_client me mata
import select
import os, signal
import sys
import jsockets

Sock = jsockets.socket_tcp_bind(1820)
if Sock is None:
    print('could not open socket')
    sys.exit(1)
# Sock.setblocking(0) # revisar si es necesario

inputs = [Sock]

while inputs:
    readable,writable,exceptional = select.select(inputs,[],inputs)
    for s in exceptional: # cerramos sockets con error
        print('Cliente desconectado (error)', file=sys.stderr)
        inputs.remove(s)
        try:
            s.close()
        except:
            pass
    for s in readable:
        if s is Sock:
            conn, addr = s.accept()
            print(f'Cliente conectado desde {addr}', file=sys.stderr)
            inputs.append(conn)
        else: # leo datos del socket
            try:
                data = s.recv(1024*1024)
            except:
                data = None
            if not data: # EOF, cliente se desconectó
                print('Cliente desconectado', file=sys.stderr)
                inputs.remove(s)
                s.close()
            else: # Hago eco como debe ser
                try:
                    s.send(data)
                except:
                    print('Cliente desconectado (error)', file=sys.stderr)
                    inputs.remove(s)

