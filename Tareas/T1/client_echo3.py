#!/usr/bin/python3
import jsockets
import sys
import threading

if len(sys.argv) != 4:
    print('Usage: ' + sys.argv[0] + ' size host port < input_file > output_file')
    sys.exit(1)

size = int(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])
finished_send = False
sent = 0
recieved = 0

s = jsockets.socket_tcp_connect(host, port)
if s is None:
    print('Could not open socket')
    sys.exit(1)

send_lock = threading.Lock()

def Rdr(s, block_size):
    global recieved
    while True:
        with send_lock:
            if finished_send and recieved >= sent:
                break
        try:
            data = s.recv(block_size)
            if not data:
                break
        except OSError as e:
            print(f"Socket error: {e}", file=sys.stderr)
            break
        recieved += len(data)
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

reader_thread = threading.Thread(target=Rdr, args=(s, size))
reader_thread.start()

while True:
    content = sys.stdin.buffer.read(size)
    if not content:
        with send_lock:
            finished_send = True
        break
    try:
        s.send(content)
    except ConnectionResetError:
        print("Error: La conexión fue restablecida por el servidor", file=sys.stderr)
        break
    except OSError as e:
        print(f"Error de socket: {e}", file=sys.stderr)
        break
    sent += len(content)

reader_thread.join()
s.close()
sys.exit(0)

