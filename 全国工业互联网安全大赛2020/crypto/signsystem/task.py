from Crypto.Util.number import getPrime, bytes_to_long
from gmpy2 import lcm,invert
import SocketServer
import signal,os,random,string
from hashlib import sha256

from secret import FLAG

def genKey():
    e = 65537
    p = getPrime(2048)
    q = getPrime(2048)
    N = p*q
    s = lcm(lcm(p-1,q-1),lcm(q+1,p+1))
    d = invert(e,s)
    return e,d,N


def encrypt(m,e,N):
    if e == 0:
        return 2
    t1 = 2
    t2 = m
    e = bin(e)[3:]
    for i in e:
        tk  = (t2*t1 - m)%N
        sk = (t2*t2 - 2)%N
        rk = (m*t2*t2-t2*t1-m)%N
        if i == '0' :
            t2 = sk
            t1 = tk
        else:
            t2 = rk
            t1 = sk
    return t2
class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def dorecv(self,sz):
        try:
            return int(self.request.recv(sz).strip())
        except:
            return 0

    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass


    def handle(self):
        signal.alarm(200)
        if not self.proof_of_work():
            return
        secret = bytes_to_long(os.urandom(48))
        self.dosend("Welcome to the Signature System.")
        self.dosend('You can sign any message you want and if you give me the secret\'s signature I will give you the flag.\n')   
	e,d,N = genKey()
        
        self.dosend('The pulickey is '+str(e)+" "+ str(N)+'\n')
	self.dosend('The secret is '+str(secret)+'\n')
        for i in range(4):	
            self.dosend("Tell me the plaintext: ")
            pt = self.dorecv(1500)
            if pt == 0:
                break
            if pt == secret:
                self.dosend('NO! You can not sign the secret!')
                break
            sig = encrypt(pt,d,N)
            self.dosend('The signature is ' + str(sig) + '\n')
        self.dosend('Tell me the secret\'s signature and I will give you the flag.\n')
        sig = self.dorecv(1500)
        if(encrypt(sig,e,N) == secret):
            self.dosend('You are smart! The flag is '+FLAG + '\n')
        self.request.close()


class ForkingServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10004
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
