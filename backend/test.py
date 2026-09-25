import sys
try:
    import adk
    print("adk imported")
    print(dir(adk))
except Exception as e:
    print(e)
