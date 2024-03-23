import os

def read_onoffpermission() -> bool:
    if os.path.exists("onoff.txt"):
        with open('onoff.txt', 'r') as f:
            if f.read() == "1":
                return True
            else:
                return False
    else:
        open('onoff.txt', 'x')
        return False


def write_onoffpermission(wr: bool):
    if wr == True:
        with open('onoff.txt', 'w') as f:
            f.write('1')
    else:
        with open('onoff.txt', 'w') as f:
            f.write('0')
