import time

# timer decorator
def timerfunc(func):
    def function_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "[{func}] took {time} sec. to complete"
        print(msg.format(func=func.__name__, time=round(runtime, 4)))
        return value
    return function_timer

@timerfunc
def benchmark_test():
    for i in range(10009):
        y = i**2

if __name__ == '__main__':
    benchmark_test()