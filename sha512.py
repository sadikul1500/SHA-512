import math

def stringToBinary(s):
    return ' '.join('{0:08b}'.format(ord(x), 'b') for x in s)


def intToBinary(x, y):
    if y == 128:
        return "{0:0128b}".format(x)

    if y == 64:
        return "{0:064b}".format(x)


def reform(s1, s2):
    n = int((len(s1) + len(s2)) % 1024)
    if n == 0:
        return s1 + s2
    else:
        s1 += '1' + format(0, 'b').zfill(1023 - n) + s2
        print(len(s1))
        return s1


def ROTR(s, x):
    return s[len(s) - x:] + s[:len(s) - x]


def SHR(s, x):
    st = '0000000'

    return st[:x] + s[:len(s) - x]  # s[x:] + st[:x]


def xor(a, b):
    s = ''

    for i in range(len(b)):
        if a[i] == b[i]:
            s += '0'
        else:
            s += '1'
    return s


def sigma1(s):
    x = xor(ROTR(s, 19), ROTR(s, 61))
    return xor(x, SHR(s, 6))


def sigma0(s):
    x = xor(ROTR(s, 1), ROTR(s, 8))
    return xor(x, SHR(s, 7))


def floatToBinary(myNumber, places):
    a, b = str(myNumber).split(".")
    b = '.' + b
    b = float(b)
    out = ''

    for x in range(places):
        a, b = str(b * 2).split('.')
        b = '.' + b
        b = float(b)
        out += a

    return out


def chc(m, n, o):
    s = ''
    for i in range(len(m)):
        if m[i] == '1':
            s += n[i]
        else:
            s += o[i]

    return s


def maj(m, n, o):
    s = ''
    for i in range(len(m)):
        s += str((int(m[i]) & int(n[i])) ^ (int(m[i]) & int(o[i])) ^ (int(n[i]) & int(o[i])))

    return s


def s512To_a(m):
    x = xor(ROTR(m, 28), ROTR(m, 34))
    return xor(x, ROTR(m, 39))


def s512To_e(m):
    x = xor(ROTR(m, 14), ROTR(m, 18))
    return xor(x, ROTR(m, 41))


def hexToBin(s):
    qw = bin(int(s, 16)).zfill(64)
    a, b = qw.split('b')

    l = len(b)

    for i in range(64 - l):
        b = '0' + b

    return b


Key = []
#file1 = tk.filedialog.askopenfilename()
with open('key.csv', 'r+') as f:
    for line in f.readlines():
        Key.append(hexToBin(line[2:18]))

f.close()


def additionModulo(s1, s2):
    x = 0

    for i in range(len(s1)):
        if s1[i] == '1':
            x += int(math.pow(2, len(s1) - 1 - i))

    y = 0

    for i in range(len(s2)):
        if s2[i] == '1':
            y += int(math.pow(2, len(s2) - 1 - i))

    return intToBinary(int((x + y) % (2 ** 64)), 64)

#************************************************main function starts*******************************************************
a = "0110101000001001111001100110011111110011101111001100100100001000"
b = "1011101101100111101011101000010110000100110010101010011100111011"
c = "0011110001101110111100110111001011111110100101001111100000101011"
d = "1010010101001111111101010011101001011111000111010011011011110001"
e = "0101000100001110010100100111111110101101111001101000001011010001"
f = "1001101100000101011010001000110000101011001111100110110000011111"
g = "0001111110000011110110011010101111111011010000011011110101101011"
h = "0101101111100000110011010001100100010011011111100010000101111001"

H = a + b + c + d + e + f + g + h

# DONE FOR INPUT TXT FILE


# data = '' #input("Enter your data")
'''with open('data.txt', 'r') as f:
    data.append(f.read()) data += f.read() '''
#file2 = tk.filedialog.askopenfilename()
fh = open('data.txt', encoding='ascii', errors='ignore')
data = fh.read()
# f.close()
# print(data)
bin_data = stringToBinary(data)
bin_data = bin_data.replace(" ", "")
length = intToBinary(len(bin_data), 128)

final = reform(bin_data, length)
N = int(len(final) / 1024)
print(N)

# ***************** round function starts ******************

for i in range(N):
    M = ''
    M += final[i * 1024:(i + 1) * 1024]

    W = []

    for j in range(16):
        W.append(M[j * 64:(j + 1) * 64])

    for j in range(16, 80):
        st = ''
        st += additionModulo(sigma1(W[j - 2]), sigma0(W[j - 15]))
        st = additionModulo(st, W[j - 7])
        st = additionModulo(st, W[j - 16])
        W.append(st)

    for j in range(80):
        t2 = additionModulo(s512To_a(a), maj(a, b, c))

        t1 = additionModulo(h, chc(e, f, g))
        t1 = additionModulo(t1, s512To_e(e))
        t1 = additionModulo(t1, W[j])
        t1 = additionModulo(t1, Key[j])

        h = g
        g = f
        f = e
        e = additionModulo(d, t1)
        d = c
        c = b
        b = a
        a = additionModulo(t1, t2)

    q = ''

    q += additionModulo(H[:64], a)
    q += additionModulo(H[64:64 * 2], b)
    q += additionModulo(H[64 * 2:64 * 3], c)
    q += additionModulo(H[64 * 3:64 * 4], d)
    q += additionModulo(H[64 * 4:64 * 5], e)
    q += additionModulo(H[64 * 5:64 * 6], f)
    q += additionModulo(H[64 * 6:64 * 7], g)
    q += additionModulo(H[64 * 7:64 * 8], h)

    H = q

    a = H[:64]
    b = H[64:64 * 2]
    c = H[64 * 2:64 * 3]
    d = H[64 * 3:64 * 4]
    e = H[64 * 4:64 * 5]
    f = H[64 * 5:64 * 6]
    g = H[64 * 6:64 * 7]
    h = H[64 * 7:64 * 8]

result = ''

for i in range(128):
    p, qw = hex(int(H[i * 4:(i + 1) * 4], 2)).split('x')
    result += qw

print(result)
#root.geometry("100x100")
#msg = tk.Message(root, text=result)

#msg.pack()
#root.mainloop()