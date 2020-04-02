import math

def to_int(s:str) -> int:
    try:
        n = int(s)
        return n
    except:
        return None

print(to_int('a42'))