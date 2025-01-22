# Timestrike

Python library for timing attacks

## Usage

The library provides two functions: `length` to obtain the length of the key, and `key` to obtain its content.

## Examples

```
import socket
import time
from timestrike import *

def measure_time(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 1337))
        s.sendall(message.encode())
        start_time = time.time()
        s.recv(1024)
        end_time = time.time()
        response_time = end_time - start_time
        s.close()
        return response_time

l = length(measure_time, chars=chars, sample=3)
k = key(measure_time, l, sample=3)
print(k)
```
