from Modules import BinListUtil as binop

def __BitConvert(message:str):
    #convert message into unicode
    charcode = [ord(c) for c in message]

    bytes = []
    #convert unicode message into 8 bit long lists of binary
    for char in charcode:
        bytes.append(bin(char)[2:].zfill(8))

    bits = []
    #convert bytes into a continuous list of bits as integers
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))

    return bits

def __BinToHex(value):
  #takes list of 32 bits
  #convert to string
  value = ''.join([str(x) for x in value])
  #creat 4 bit chunks, and add bin-indicator
  binaries = []
  for d in range(0, len(value), 4):
    binaries.append('0b' + value[d:d+4])
  #transform to hexadecimal and remove hex-indicator
  hexes = ''
  for b in binaries:
    hexes += hex(int(b ,2))[2:]
  return hexes

def __fillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else: 
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits

def __chunk(bits, chunk_length=8):
    # divides list of bits into desired byte/word chunks, 
    # starting at LSB 
    chunks = []
    for b in range(0, len(bits), chunk_length):
        chunks.append(bits[b:b+chunk_length])
    return chunks

##hardcoded values
#initial hash values
h = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

#round constants
k = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5',
     '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174', 
     '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da', 
     '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7','0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', 
     '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', 
     '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', 
     '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3',
     '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2']

#convert above values into usable binary
def __valueInit(values):
    #hex 2 binary string minus '0b' binary indicator
    binaries = [bin(int(v, 16))[2:] for v in values]
    #convert fron string to list of 32 bit lists
    words=[]
    for binary in binaries:
        word=[]
        for b in binary:
            word.append(int(b))
        words.append(__fillZeros(word, 32, 'BE'))
    return words

def __messagePreprocess(message:str):
    #message to bits
    bits = __BitConvert(message)

    length = len(bits)

    message_len = [int(b) for b in bin(length)[2:].zfill(64)]

    #message binary always appended with 1
    bits.append(1)

    ##set binary # of bits to multiple of 512 for chunking
    ##last 64 bits is the message_length

    #448 = 512 - 64: pad to 448 with zeros
    if length < 448:
        bits = __fillZeros(bits,448,'LE')
        #append message_len binary
        bits = bits + message_len
        #bits is already 512 bits long so no chunking is necissary
        return [bits]
    else:
        #loop until bits length is multiple of 512
        length = len(bits)
        while ((length+64) % 512 != 0):
            bits.append(0)
            length+=1
        #add 64 bit message length
        bits = bits + message_len
        #chunk time
        return __chunk(bits, 512)
####
## The Algorithm
####
def Hash256(message:str):

    k1 = __valueInit(k)

    h0, h1, h2, h3, h4, h5, h6, h7 = __valueInit(h)

    chunks = __messagePreprocess(message)

    for chunk in chunks:
        #message schedule, w
        #list of 32 bit words, 16 words total
        w = __chunk(chunk, 32)
        #extend 'w' to 64 words (64 - 16 = 48)
        for n in range(48):
            #pads with 32 zeroes. Zero word
            w.append(32 * [0])
        #fancy bitwise operators
        for i in range(16,64):
            s0 = binop.XORXOR(binop.rotr(w[i-15], 7), binop.rotr(w[i-15], 18), binop.shr(w[i-15], 3))
            s1 = binop.XORXOR(binop.rotr(w[i-2],17), binop.rotr(w[i-2], 19), binop.shr(w[i-2], 10))
            w[i] = binop.binAdd(binop.binAdd(binop.binAdd(w[i-16], s0), w[i-7]), s1)

            #intermediary
        ai = h0
        bi = h1
        ci = h2
        di = h3
        ei = h4
        fi = h5
        gi = h6
        hi = h7

        for j in range(64):
            S1 = binop.XORXOR(binop.rotr(ei, 6), binop.rotr(ei, 11), binop.rotr(ei, 25))
            ch = binop.XOR(binop.AND(ai, bi), binop.AND(binop.NOT(ei), gi))
            temp1 = binop.binAdd(binop.binAdd(binop.binAdd(binop.binAdd(hi, S1), ch), k1[j]), w[j])
            S0 = binop.XORXOR(binop.rotr(ai, 2), binop.rotr(ai, 13), binop.rotr(ai, 22))
            m = binop.XORXOR(binop.AND(ai, bi), binop.AND(ai, ci), binop.AND(bi, ci))
            temp2 = binop.binAdd(S0, m)
            hi = gi
            gi = fi
            fi = ei
            ei = binop.binAdd(di, temp1)
            di = ci
            ci = bi
            bi = ai
            ai = binop.binAdd(temp1, temp2)

        h0 = binop.binAdd(h0, ai)
        h1 = binop.binAdd(h1, bi)
        h2 = binop.binAdd(h2, ci)
        h3 = binop.binAdd(h3, di)
        h4 = binop.binAdd(h4, ei)
        h5 = binop.binAdd(h5, fi)
        h6 = binop.binAdd(h6, gi)
        h7 = binop.binAdd(h7, hi)
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += __BinToHex(val)
    return digest