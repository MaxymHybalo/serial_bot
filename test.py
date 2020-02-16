import time
import logging

logging.basicConfig(level=logging.CRITICAL)
start = time.time()
# print('[Start benchmarks]')
import test.benchmark
end = time.time() - start
print('[All time exec: {end}]'.format(end=end))