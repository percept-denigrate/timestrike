import time
from string import printable

def get_length(measure_time, chars=printable, sample=1, selector=min, max_len=64):
    times = [[] for _ in range(max_len)]
    for _ in range(sample):
        for l in range(max_len):
            message = chars[0] * l
            times[l].append(measure_time(message))
    return max(range(max_len), key=lambda l: selector(times[l]))

def get_key(measure_time, length=None, chars=printable, sample=1, selector=min, initial_key="", print_keys=False):
    if length is None:
        length = get_length(measure_time, chars=chars, sample=sample, selector=selector, max_len=64)
    for _ in range(length - len(initial_key)):
        times = {c:[] for c in chars}
        for _ in range(sample):
            for char in chars:
                message = initial_key + char + chars[0] * (length - len(initial_key) - 1)
                response_time = measure_time(message)
                times[char].append(response_time)
        selected = max(times, key=lambda c: selector(times[c]))
        initial_key += selected
        if print_keys:
            print(initial_key)
    return initial_key
