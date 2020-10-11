# Decrypt-the-Message - Poem Codes

这是一种比较奇特的加密方式，叫做Poem Codes，详见：http://wmbriggs.com/post/1001/  

加密过程如下：  

（1）就其算法而言，去诗歌头一个单词，全部罗列出来，然后所有单词的字母按字母表排序并编码，如第一个a为1，第二个a为2，如果没有a了就看b，第一个b为3，第二个b为4，一直排列下去...   

（2）将要加密的信息的字母每18个一行（不足一行的abcdef....补足）  

（3）将加密的信息第一个字母对应第一步的编码数字，到第二步生成的字母表中取某列。  

（4）分组即成加密信息。  

解密过程非常复杂，不过，有人已经写好了解密工具，详见：https://github.com/abpolym/crypto-tools/tree/master/poemcode  


Exp:
```python
# Poem Codes

import sys
import itertools
from os import listdir
from os.path import isfile, join

abc='abcdefghijklmnopqrstuvwxyz'

def loadlist(infile):
    tlist = []
    for line in open(infile, 'r'):
        for w in line.split(): 
            tlist.append(w.lower())
    return tlist

def encrypt(code, poem, msg):
    # Load all words of the poem into a temporary list
    twords = loadlist(poem)

    # Select only those words specified in the code in a new list
    pwords = ''
    for c in code: pwords += twords[c].lower()
    plen = len(pwords)

    # We can only support encoding all alphabetical letters, a key length greater len(abc) is not reasonable here
    if plen > len(abc): sys.exit(3)

    # Assign an index for each letter in the key based on the alphabet
    pcode = [None] * plen
    count = 0
    while(count<plen):
        for al in abc:
            for pc, pl in enumerate(pwords):
                if al!=pl: continue
                pcode[pc]=count
                count+=1

    # Load all words of the message into a string
    mwords = ''
    for line in open(msg, 'r'):
        for w in line.split(): mwords+=w.lower()
    mlen = len(mwords)

    # Split message into chunks of size plen, append random (here alphabet) characters to fill the last chunk, if necessary
    cpairs = []
    curlen = plen
    while(curlen<mlen):
        cpairs.append(mwords[curlen-plen:curlen])
        curlen+=plen
    rword = mwords[curlen-plen:curlen]
    rlen = len(rword)
    if rlen < plen: rword += abc[:plen-rlen]
    cpairs.append(rword)

    # Encrypt the message according to the key
    cip = ''
    for i in code: cip+=abc[i]
    cip+=' '
    for i in pcode:
        for pair in cpairs:
            cip += pair[i]
        cip+=' '
    return cip

def decrypt(poem, cip):
    # Load all words of the poem into a temporary list
    twords = loadlist(poem)

    # Load all cipher chunks of the ciphertext into a list
    cwords = loadlist(cip)

    # Get the code rom the first chunk and remove it from the ciphertext list
    code = []
    for i in cwords.pop(0):
        code.append(abc.index(i))
    
    # Select only those words specified in the code in a new multi-arrayed list
    xwords = [[] for x in range(len(code))]
    for xcount, c in enumerate(code):
        tlen = c
        while(c<len(twords)):
            xwords[xcount].append(twords[c].lower())
            c+=26

    # Get all possible combinations
    for comb in itertools.product(*xwords):
        pwords = ''
        for c in comb: pwords+=c
        plen = len(pwords)

        # Rearrange the chunks according to the key
        pcode = [None] * plen
        count = 0
        while(count < plen):
            for al in abc:
                for pc, pl in enumerate(pwords):
                    if al != pl:
                        continue
                    pcode[count]=cwords[pc]
                    count+=1

        # Decrypt the ciphertext
        msg = ''
        wlen = len(pcode[0])
        for c in range(0, wlen):
            for word in pcode:
                msg += word[c]
        print(msg)

# first argument = poem
# second argument = ciphertxt or msg
if len(sys.argv) != 3: 
    print('Usage: python exp.py <poem.txt> [<cip.txt>|<msg.txt>]')
    print('Note that the poem, msg and cipher has to be alphabetic letters only. No commatas, dots, whatgives.')
    sys.exit(2)

#print encrypt([0, 5, 13, 16, 19], sys.argv[1], sys.argv[2])
decrypt(sys.argv[1], sys.argv[2])
```