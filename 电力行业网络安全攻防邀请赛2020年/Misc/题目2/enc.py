# encoding=utf-8

flag_enc = open("./flag_enc.hex", "wb+")


def file_encode(flag):
    i = 1
    while True:


        byte_str = flag.read(1)
        if (byte_str == b''):
            exit()

        byte_str = hex_encode(byte_str)
        file_write(flag_enc, byte_str)
        # print(byte_str, end="")
        i = i + 1

def hex_encode(byte_str):

    tmp = int.from_bytes(byte_str, byteorder="big")
    if (tmp % 2 == 0):
        tmp = (tmp + 1) ^ 99
    else:
        tmp = (tmp - 1) ^ 99
    tmp = bytes([tmp])
    return tmp

def file_write(flag_enc, byte_str):
    flag_enc.write(byte_str)



if __name__ == '__main__':
    with open("./flag.png", "rb") as flag:
        file_encode(flag)
    flag_enc.close()