import sys
log = open('ATI45.txt', 'rb')
a = log.readline()
print(str(a))
print(sys.getsizeof(a))