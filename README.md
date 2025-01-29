# Timestrike

Python library for timing attacks

## Usage

The library provides two functions: `get_length` to obtain the length of the key, and `get_key` to obtain its content. They only require the user to define the function that gives the processing time of a given string.

## Examples

If the target is a server accepting TCP connections:
```
import socket
import time
from timestrike import get_key

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

k = get_key(measure_time, sample=3)
print(k)
```

If the target is a binary that checks a pin number (taken from [picoCTF](https://play.picoctf.org/practice/challenge/298)):
```
import subprocess
import time
from timestrike import get_key

elf_file = './pin_checker'

def measure_time(pin):
    process = subprocess.Popen(
        elf_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    start = time.time()
    process.communicate(input=f"{pin}\n")
    end = time.time()
    return end - start

print(get_key(measure_time, chars="1234567890"))
```
