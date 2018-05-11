




def shiftRows(state):
        """Performs shiftRows operation on the state."""

        # put your code here
        orgstate=state
        newstate = bytearray(16)
        newstate[4:7] = state[5:8]
        newstate[7] = state[4]
        newstate[10:12] = state[8:10]
        newstate[8:10] = state[10:12]
        newstate[13:16] = state[12:15]
        newstate[12] = state[15]
        state[0:16] = newstate[0:16]
        return state

for i in range(16):
	a = shiftRows(16)
	a[i]=i
	print(a)
s=shiftRows(a)
print(s)
