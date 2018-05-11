### This is a template file for Project 3.
##
##  Please implement the provided function and assure that your code
##  works correctly. Please submit your code together with the 
##  requested answers through blackboard
##
##  Name: <Mehmet Sinan INCI>
##  Date: <03/19/2015>
##

from binascii import hexlify, unhexlify
from msi_aes import *
import struct

# Problem 3: 
ciphertext1 = int.to_bytes(0xe719f8ab9e0b846f0cf2e5c32a0e5b45,16,'big')
faultytext1 = int.to_bytes(0xe719f86f9e0beb6f0c97e5c38b0e5b45,16,'big')

ciphertext2 = int.to_bytes(0x78f272c7cf5383085fa240236d97130f,16,'big')
faultytext2 = int.to_bytes(0x78f27277cf53e7085f944023fa97130f,16,'big')

c1 = ciphertext1
f1 = faultytext1
c2 = ciphertext2
f2 = faultytext2

def AESFaultAttack(ct,ft):
#def afa(ct,ft):
    ''' performs a key recovery attack on four bytes of the key
        using a correct and a faulty AES ciphertext.
        the function returns a list of subkey candidates.'''
# run the following if you don't know the locations of the faulty bytes..
    '''
    n=0
    faultybytes = bytearray(4)
    
    for i in range(len(ct)):
        #print(ct[i],ft[i])
        if ct[i]!=ft[i]:
            faultybytes[n]=i
            n +=1
    print(hexlify(faultybytes))
    '''
#############################################################
    
    candidates = bytearray()
    faultybytes = [3,6,9,12]

#    for j in faultybytes:
#        for k in range(256):
#            delta = iSbox[ct[j]^k] ^ iSbox[ft[j]^k]
#            if k==delta:
#                print(delta)
#                candidates.append(k)

# if k2==delta2:
# print('Second byte match! Checking third byte')
# if k4==delta4:
# print('Forth byte match! Adding the possible key!')
# print(k1,k2,k3,k4)

    for k12 in range(256):
        ct12 = iSbox[ct[12]^k12]
        ft12 = iSbox[ft[12]^k12]
        delta12 = ct12 ^ ft12
        for k9 in range(256):
            ct9 = iSbox[ct[9]^k9]
            ft9 = iSbox[ft[9]^k9]
            delta9 = ct9 ^ ft9
            if (delta12 == delta9):
                for k6 in range(256):
                    ct6 = iSbox[ct[6]^k6]
                    ft6 = iSbox[ft[6]^k6]
                    delta6 = ct6 ^ ft6
                    if (mult3(delta12) == delta6):
                        for k3 in range(256):
                            ct3 = iSbox[ct[3]^k3]
                            ft3 = iSbox[ft[3]^k3]
                            delta3 = ct3 ^ ft3
                            if (mult2(delta12) == delta3):
                                #print('match on 4th level')
                                # mult2 is GF multiplication from aes with 2, mult3 is for multiplication with 3
                                #myarray = [k3,k6,k9,k12]
                                candidates.append(k3)
                                candidates.append(k6)
                                candidates.append(k9)
                                candidates.append(k12)

    #print(hexlify(candidates))

    return candidates

def keyfinder(cand1, cand2):
    key = []
    c1len = len(cand1)
    c2len = len(cand2)
    i = 0
    j = 0
    print('number of candidates from the first and the second pair are',c1len//4,'and',c2len//4)
    while i <(c1len):
        while j <(c2len):
            c1k3 = cand1[i]
            c1k6 = cand1[i+1]
            c1k9 = cand1[i+2]
            c1k12 = cand1[i+3]

            c2k3 = cand2[j]
            c2k6 = cand2[j+1]
            c2k9 = cand2[j+2]
            c2k12 = cand2[j+3]
            
            #print('i is',i,' and j is ',j)
            if (c1k3 == c2k3 and c1k6 == c2k6 and c1k9 == c2k9 and c1k12 == c2k12):
                print('FOUND A MATCH! the key is ',cand2[j],cand2[j+1],cand2[j+2],cand2[j+3])
                temp_array = [cand2[j],cand2[j+1],cand2[j+2],cand2[j+3] ]
                key.append(temp_array)
            j=j+4
        #print('i is',i,' and j is ',j)
        i=i+4
        j=0
        #print(i)
    print('key is ',key)
    return key

# first pair test

print('Testing the first c1-f1 pair and finding candidates')
cand1 = AESFaultAttack(c1,f1)
print('Found all the possible keys for c1-f1 pair!')
print('Testing the first c2-f2 pair and finding candidates')
cand2 = AESFaultAttack(c2,f2)
print('Found all the possible keys for c2-f2 pair!')


key = keyfinder(cand1,cand2)



# Note: after performing the attack twice, you can find the
#       matching candidates for both cases. this will leave
#       you with only one remaining candidate.

