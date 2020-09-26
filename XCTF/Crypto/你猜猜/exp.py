with open('你猜猜.txt', 'r') as f:
    with open('你猜猜_bytes.zip', 'wb') as fw:
        content = f.readline()
        b = b''
        j = 0
        for i in range(len(content) // 2):
            b += bytes.fromhex(content[j:j+2])
            fw.write(b)
            j += 2