name = "Dummy search"
from time import sleep

def run(username):
    global name
    for i in range(4,-1,-1):
        name = "Dummy search " + str(i+1)
        yield
        sleep(1)
    return {}