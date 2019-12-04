import utime
def performanceTest():
    endTime = utime.ticks_add(utime.ticks_ms(), 10000)
    count = 0
    while utime.ticks_ms() < endTime:
        count += 1
    print("Count: ", count)
performanceTest()