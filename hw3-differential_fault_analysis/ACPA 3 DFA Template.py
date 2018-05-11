### This is a template file for Project 3.
##
##  Please implement the provided function and assure that your code
##  works correctly. Please submit your code together with the 
##  requested answers through blackboard
##
##  Name: <your name>
##  Date: <submission date>
##


# Problem 3: 
ciphertext1 = int.to_bytes(0xe719f8ab9e0b846f0cf2e5c32a0e5b45,16,'big')
faultytext1 = int.to_bytes(0xe719f86f9e0beb6f0c97e5c38b0e5b45,16,'big')

ciphertext2 = int.to_bytes(0x78f272c7cf5383085fa240236d97130f,16,'big')
faultytext2 = int.to_bytes(0x78f27277cf53e7085f944023fa97130f,16,'big')

def AESFaultAttack(ct,ft):
    ''' performs a key recovery attack on four bytes of the key
        using a correct and a faulty AES ciphertext.
        the function returns a list of subkey candidates.'''

    return candidates

# Note: after performing the attack twice, you can find the
#       matching candidates for both cases. this will leave
#       you with only one remaining candidate.
