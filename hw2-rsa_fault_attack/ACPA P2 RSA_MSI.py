### This is a template file for efficient modular exponentiation functions
### and a reference implementation of RSA PKCS #1, v2.1 encryption.
##
##  Please implement the provided functions and assure that your code
##  works correctly for the example given below
##
##  Name: <Mehmet Sinan INCI>
##  Date: <02/19/2015>
##

import time
import sys
#import binascii
#import bitarray 
sys.setrecursionlimit(4*2048)



def my_pow_SqMul(b,e,m):
    ''' Performs modular exponentiation (b^e mod m)
        using the square and multiply algorithm'''

    # put your code here
    """ Computes b^e mod m using the square and multiply algorithm"""
    if e == 0:
        #print('exponent is zero')
        return 1
    
    ## enter your source code here
    
    r = 1
    bn = bin(e)[2:]     # convert the exponent to binary format, discard the prefix ‘0b’
    i = 0
    while (i < len(bn)):
        r = (r * r) % m     # square is done automatically for every exponent digit
        if int(bn[i]) != 0:     # multiply is done only if the exponent is 1
            r = (r * b) % m
        i = i + 1    
    return r

def findl(bine,k):      # my function that finds the longest exponent sequence that ends with 1
    seq = 0b0
    

    if len(bine) < k :
        k = len(bine)
        #print('e was so small, it is ',k)
    
    while k>= 0:
        if (bine[k-1]) == '0':
            #print(k, ' th exponent is zero')
            k = k - 1
            #print('reduced k is ', k)
        else:
            seq = bine[0:k]
            #print('seq is ',seq)
            k=-1
        seq = str (seq)
    return seq


def my_pow_SlWin(x,e,n,k=4):
    ''' Performs modular exponentiation (b^e mod m)
        using the sliding window algorithm with window size k'''

    # put your code here
    y=0
    # precomputation
    g = [0] * 2**k
    g[0] = 1 %n
    g[1] = x %n
    g[2] = x**2 %n
    bine = bin(e)[2:]
    #print('precalculated g is ',g)
    #print('binary e is ',bine)

    myrange = 2**(k-1)
    for i in range(myrange-1):
        g[2*(i+1)+1] = (g[2*(i+1)-1] * g[2] )%n
        
    #print('precalculated g after loop is ',g)

    y = 1
    # exponentiation
    i = 0
    elen = len(bine)
    #print('length of exponent is ',elen)
    while (i<elen):
        if int(bine[i]) == 0 :
            #print('exponent is zero, doing only square')     # string index out of range if e larger than 10???
            y = (y**2) % n
            i = i +1
        else:
            #print('exponent is ONE, looking for longest sequence')
            bine=bin(e)[2:]
            seq = findl(bine[i:],k)
            seq = str (seq)
            #print ('type of the main func seq is ',type(seq))
            l = len(seq)
            temp_ex = 2**l
            #print('m to the l is ',temp_ex)
            y = (y**temp_ex) % n
            idx = int(seq,2)
            #print ('index is ',idx)
            y = (y * g[idx] ) % n
            i=i+l
        #print('current y is ',y)   
    y = y % n
    return y
# test my_pow_SlWin(2,5,5,3)




def MGF(seed,maskLen):
    '''returns a mask of length maskLen, generated from seed using SHA-256'''
    import hashlib
    from math import ceil
    
    #seed = bytearray([1,2,3])
    # .digest_size kac blok (byte) oldugunu gosteriyor
    #myhash = hashlib.sha256(seed)

    #put your code here

    hLen = hashlib.sha256(seed).digest_size
    if maskLen > 2**32 * hLen:
        raise ValueError("mask too long")
    T=bytearray()
    for counter in range(int(ceil(maskLen / (hLen*1.0)))):
        #C = I2OSP (counter, 4)
        #T = T || Hash(mgfSeed || C)
        #C = long_to_bytes(counter) *** error
        C = bytes([(((0xff << i*8) & counter) >> i*8) for i in reversed(range(counter.bit_length()))])
        #print(C)
        C = (b'\x00'*(4 - len(C))) + C  
        #C = int.from_bytes(C, byteorder='big', signed=False)
        #print(C)

        assert len(C) == 4, "counter was too big"
        T += hashlib.sha256(seed + C).digest()
    assert len(T) >= maskLen, "generated mask was too short"
    return T[:maskLen]



def RSAESencrypt(N,e,m,L=bytearray()):
    '''Performs RSA PKCS #1 v2.1 encryption using the public key <N,e>
        on message m (optinal: label L). Ciphertext c is returned.
        N and e are integers, m, L, and c are byte arrays'''

    import hashlib
    import os
    #tempm = int.from_bytes(m, byteorder='big', signed=False)
    #print(tempm)
    mLen = len(m)
    hLen = hashlib.sha256().digest_size # since we use SHA256

    # put your code here:
    
    # check lengths
    k = N.bit_length()//8
    #print('k is ', k)
    if mLen > k-11:
        print('message too long')
        raise IOError

    # generate DB
    PS = bytearray()
    #prePS = os.urandom(k-mLen-3)
    for j in range(k-mLen-3):
        temp = os.urandom(1)
        while temp == b'\x00':
            temp = os.urandom(1)
            #print('we have found a zero!')
        PS = PS + temp
    #print('PS is ',len(PS))
    
    #PS = bytearray(k-mLen-3)
    #PS = (k-mLen-3)*b'\x05'
    #print(PS,'\n',len(PS))

    # seeding and masking
    # generate EM
    EM = b'\x00' + b'\x02' + PS + b'\x00' + m
    #zero = bytearray([0])
    #templen = len(EM)
    #for i in range(templen):
    #    while EM[i]!=0:
    #        i+=1
    #       print(i)
    #print(EM,'\n len of EM is \n',len(EM))
    #print('PS is ',PS)
    #print('m is ',m)
    # perform encryption
    c = bytearray()
    m = int.from_bytes(EM, byteorder='big', signed=False)
    #print('plain m is ',m)
    c = pow(m,e,N)
    #print('integer c is ',c)
    cLen = c.bit_length()//8
    #print('integer c is ',c)
    try:
        C= bytearray.fromhex(hex(c)[2:])
    except ValueError:
        C= bytearray.fromhex('0' + hex(c)[2:])
    #C = bytes([(((0xff << i*8) & c) >> i*8) for i in reversed(range(cLen))])
    #print('bytearray c is ',C)
    #print('c len is ',len(C))
    #print('EM 0 - 1 - 2 are ',EM[0],EM[1],EM[2])
    return C


def RSAESdecrypt(N,d,c,L=bytearray()):
    '''Performs RSA PKCS #1 v2.1 decryption using the private key <N,d>
        on ciphertext c (optinal: label L). Message m is returned.
        N and d are integers, m, L, and c are byte arrays'''

    import hashlib
    import os
    from math import ceil

    cLen = len(c)
    #print(cLen)
    hLen = hashlib.sha256().digest_size # since we use SHA256

    # put your code here:
    # check lengths

    k = N.bit_length()//8
    if k < 11:
        print ('decryption error')
        raise IOError
    # decrypt C
    #print('bytearray c is ',c)
    #print('c len is ',len(c))
    c = int.from_bytes(c, byteorder='big', signed=False)
    #print('integer c is ',c)
    
    m = pow(c,d,N)
    #print('EM is ',m)
    mLen = ceil(m.bit_length()/8)
    zero = bytearray([0])
    try:
        EM= bytearray.fromhex(hex(m)[2:])
    except ValueError:
        EM= bytearray.fromhex('0' + hex(m)[2:])
    EM = zero + EM
    #print('EM 0 - 1 - 2 are ',EM[0],EM[1],EM[2])
    
    # separate EM

    invalid = any([EM[0]!=0, EM[1]!=2])
    if invalid :
        print('decryption error')
        raise IOError
        
    # ps size is k-mLen-3
    
    # remove masks
    #print(EM,len(EM))
    EM = EM[2:]
    templen = len(EM)
    #print(EM)
    i=0
    while EM[i]!=0:
        i+=1
        #print(i)
        
    #print(type(len(EM)))
    mylen = len(EM)
    m = EM[i+1:mylen]   
    #print(EM,len(EM))
    #m = EM[k-mLen-3:len(EM)]
    #print('PS is ',PS)
    #print('m is ',m)

    
    # check DB

    #Note.  Care must be taken to ensure that an opponent cannot
    #distinguish the different error conditions in Step 3.g, whether by
    #error message or timing, or, more generally, learn partial
    #information about the encoded message EM.  Otherwise an opponent may
    #be able to obtain useful information about the decryption of the
    #ciphertext C, leading to a chosen-ciphertext attack such as the one
    #observed by Manger
    #m=bytearray.fromhex(hex(m)[2:])
    
    return m
    
    
        
p =  997782014483135516947467112733783206034059987091508997470391422588302757009297888172824321316039986332404368187672035334285863264469832007564899663393813987428733469948510589362567714925225591609164647780163771437334778893745924369236957875430167009790722454797434933978389194431730946950351883503681 
q = 79301961686790288135761596161932125982627215111620602465105295605167614622099617732042554017601029601972431354155023876998569040821697397911153196884814759437163993503206804558864234356549520950879755905643095880867184872343043391321834768955404845085269931482274291437512222693097323499756682477811051
#p = 8176662165573700613347344450959887037086515168356394479546398903326976319674343656956828452558146536261756580874692178418735952635936011308339369316896181
#q = 13062362680240858986014063047218740765842583586324085493117801839987719301360641696613806125427125208683501703668298486807198605540347486024024409678675789

N = p*q

b = 3
e = 2**1000-1
m = N

tic = time.clock()
out = pow(b,e,m)
toc = time.clock()
Tpow = toc-tic

tic = time.clock()
out2 = my_pow_SqMul(b,e,m)
toc = time.clock()
Tsqmul=toc-tic

tic = time.clock()
out3 = my_pow_SlWin(b,e,m)
toc = time.clock()
Tslwin=toc-tic


if(out == out2):
    print('Square and multiply: works (in ',Tsqmul,'s)')
else:
    print('Square and multiply: failed')

if(out == out3):
    print('Sliding Window:      works (in ',Tslwin,'s)')
else:
    print('Sliding Window:      failed')




# Testing RSA encryption and decryption
# don't mess with tese numbers:
p = 8176662165573700613347344450959887037086515168356394479546398903326976319674343656956828452558146536261756580874692178418735952635936011308339369316896181
q = 13062362680240858986014063047218740765842583586324085493117801839987719301360641696613806125427125208683501703668298486807198605540347486024024409678675789
N = p*q
e = 2**16+1
d = 95305639297136535129830247353885048571790931736897092024327830574503233416208940851818667509421055075611745557004095412620624213281032376171998990351263574092801357243118351700307075125243451771395731520183667695423762834718377372357353733379277776224241008883890378073612334038347526558549705139740335907073

# Test MGF:
print('Starting MGF Test: ',end = '')
seed = bytearray()
for cnt in range(33):
    seed.append(cnt)

check = MGF(seed,42)
correct = bytearray(b'_\xf0\x98\xa3\xa9\xe7\xa9=\xc6\x04\x99\xf1\xa6\xfb\xf6\x8cW\x9c\x90B\xd6\x9cEs\x1d\xf9\xd7\xa8\x0e\xfb)\xaf\xc0\xc9\n=\x9e\x8a\x11\x18o;')
if len(check)!=42:
    print('error: wrong output length')
elif(check != correct):
    print('failed: wrong output')
else:
    print('passed')


# Test RSA Encryption and decryption:
print('Starting first RSA Test: ',end = '')

m = b'\x02\xff'
c = RSAESencrypt(N,e,m)
mp = RSAESdecrypt(N,d,c)
if (mp!=m):
    print('failed: message not recovered')
else:
    print('passed')
# DB= bytearray(b"\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$\'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\xff"

print('Starting second RSA Test: ',end = '')
m = correct
c = RSAESencrypt(N,e,m)
mp = RSAESdecrypt(N,d,c)
if (mp!=m):
    print('failed: message not recovered')
    #print(mp,'\n', m)
else:
    print('passed')
# DB= bytearray(b"\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$\'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01_\xf0\x98\xa3\xa9\xe7\xa9=\xc6\x04\x99\xf1\xa6\xfb\xf6\x8cW\x9c\x90B\xd6\x9cEs\x1d\xf9\xd7\xa8\x0e\xfb)\xaf\xc0\xc9\n=\x9e\x8a\x11\x18o;")

print('Starting first RSA Failure Test: ',end = '')

m = correct+correct+correct
try:
    c = RSAESencrypt(N,e,m)
except IOError:
    print('passed')
else:
    print('failed')

print('Starting second RSA Failure Test: ',end = '')

c = b"A\xe0\xe5\xe6G)\xbc\x04\xd3'\xe50@/\xddiy\xff\xd0\x8b\xc8U\x10p\xf5v{`\xa7\x19o\xe5\xb3X~\x10\xbf7eN\x9ey\x9f\x1d\xe9\xe8\x89\xbcxX\xee\x95\xf5\xdf\xc7M\x91\xc3\x84C\x15]a\xf9\xcf]\xb4r\x06\xb8QL\x86\x19^NF\xd2\xf6|\xeb\x10G\xc6\x0b\x87\x07\xd1O\xff(\xadk\xe1Cj\xfc\xbc=\xee\x16cc\xb69\xb3\xcb\x92 e+G\x1f\x85&~4p\xc2\x8f]\xf2\xfb\xee\xa6\xe2oJ"
try:
    m = RSAESdecrypt(N,e,c)
except IOError:
    print('passed')
else:
    print('failed')



'''
bit length of an integer:
n.bit_length()

easy os2ip (get integer representative from bytes):
int.from_bytes(b, byteorder='big', signed=False)

xor two byte lists in one line:
[i ^ j for (i,j) in zip(list1, list2)]

i2osp (get bytes from integer):
# where integer x is xLen octets long:
bytes([(((0xff << i*8) & x) >> i*8) for i in reversed(range(xLen))])

Avoid short circuit evaluation:
valid = all([condition1, condition2, ..., conditionn])
'''
