import re

with open('new.txt', 'r') as f:
    with open('Reversed.jpg', 'wb') as fw:
        text = f.readline()[::-1]
        
        i = 0
        for j in range(len(text) // 2):
            print(bytes.fromhex(text[i:i+2]))
            fw.write(bytes.fromhex(text[i:i+2]))    
            i += 2



if __name__ == '__main__':
    with open('new.txt', 'r') as f:
        with open('Reversed.txt', 'w') as fw:
            fw.write(f.readline()[::-1])