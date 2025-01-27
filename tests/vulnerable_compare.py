import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from timestrike.timing import *

password = "p4ssW0rd!"

def vulnerable_compare(message, password):
    if len(message) != len(password):
        return False
    for i in range(len(password)):
        time.sleep(1e-6)
        if message[i] != password[i]:
            return False
        time.sleep(1e-6)
    return True

def measure_time(message):
    start_time = time.time()
    vulnerable_compare(message, password)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time

k = get_key(measure_time, sample=5)
assert k == password
