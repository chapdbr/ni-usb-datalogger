import msvcrt

while True:
    if msvcrt.kbhit():
        key = ord(msvcrt.getch())
        print(key)
