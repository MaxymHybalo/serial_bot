import test.processes_benchmarks
import test.circus_flow_benchmarks

from test.timerfunc import timerfunc

test.processes_benchmarks.run()
test.circus_flow_benchmarks.run()