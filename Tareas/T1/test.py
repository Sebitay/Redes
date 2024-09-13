
import sys
size = 8

while True:
    content = sys.stdin.buffer.read(size)  # Lee 'size' bytes de stdin
    if not content:  # Si no hay más contenido, sale del bucle
        break
    print(content)