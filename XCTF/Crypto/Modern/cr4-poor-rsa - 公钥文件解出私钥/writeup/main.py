import base64

with open('flag.b64', 'r') as f:
    with open('flag.enc', 'wb') as fw:
        text = base64.b64decode(f.readline().encode())
        fw.write(text)