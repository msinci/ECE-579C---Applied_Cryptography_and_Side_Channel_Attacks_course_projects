### This is a template file for the RSA part of Project 1.
##
##  Please implement the provided functions and assure that your code
##  works correctly for the example given below
##
##  Name: <Mehmet Sinan INCI>
##  Date: <submission date>
##
# 3. Algorithms for RSA:

import math
    
# xGCD:
def xgcd(a,b):
    """
    Returns g, x, y such that g = x*a + y*b = gcd(a,b).
    """

    ## enter your source code here
    tempa = a
    tempb = b
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    g = b

  #  if x<0:     # just in case we get a negative factor we add PhiN
   #     x+=tempb    
    #if y<0:     # just in case we get a negative factor we add PhiN
     #   y+=tempb
        
    return (g,x,y)


# Square and Multiply:
def my_pow(b,e,m):
    """ Computes b^e mod m using the square and multiply algorithm"""
    if e == 0:
        print('exponent is zero')
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

# 4. Textbook RSA implementation

def RSAenc(m,e,N): # return m^e mod N
    """ Returns the RSA message of m encrypted with e and modulus N """
    return pow(m,e,N)

def RSAdec(c,d,N): # return c^d mod N
    """ Returns the RSA ciphertext of c decrypted with d and modulus N """
    
    # enter your source code here
    m = my_pow(c,d,N);
    print('m is ',m)    
    return m


def RSAkeyGen(p,q): # return N, e, d
    """ Returns RSA key parameters (N, e, d) for provided primes p, q"""

    # enter your source code here
    N = p*q
    e = 2**16 + 1
    phiN = (p-1)*(q-1)
    g,x,d = xgcd(phiN,e)
    print('N is, ', N,'\n e is ',e,'\n d is ',d)

    return (N, e, d)

# Test runs:

#test xgcd
if xgcd(5,11)!=(1, -2, 1):
    print('your euclidean algorithm is not working properly')
else:
    print('your xgcd works for (5,11). Make sure it works in other cases as well.')

# test my_pow: ensure that it returns same results as pow

#numbers:
p = 11774567196795186264890848937988269619683091795498048470488793460033796137085963964957988661149476070297371372186826196425817253890682262453606914957198881
q = 8435082675921437589517253761085461515430725753300480036958921837140523617047618083576237472912904464351693736482550242276422621440841845620675882916844183
c = 30

[N,e,d] = RSAkeyGen(p,q)

if (N,e,d) ==  (99319447778159920001802644769289751214190171219471746369568105399503650351608702457923041518347063556240051822775445641140989635531585593239649583258865907829956071074891197963112931610030508610518491862480930246526993949348986438219801715407359067159032470535825948137603879630857986202660061171530018959223, 65537, 9253468241351365969315149441709007444860844797077902304539158819741051452567599023575660947419429788888746149959059326560673859263558930563213152194617317085151740958169894864685482702391686750550924795893823238926777553265002860248685794654814225234257102062959850223777020204607169834860283991372789063553):
    print('RSAkeyGen seems to work')
else:
    print('RSAkeyGen More debugging is needed')

    
m = RSAdec(c,d,N)

if m == 11310597885049816398545519679977433463378728199797096095243215447988684185326674776649177672795946600460919164437118720537356986796341900656822495511846493834850057021845379135471208482061633332638644277381085667872908244835771738174054154239121545046201990020497167584653288486349800300413518893627258069148:
    print('RSAdec seems to work')
else:
    print('RSAdec: More debugging is needed') 

# AES in separate file
