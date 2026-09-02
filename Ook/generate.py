"""Generate Fibonacci in Brainfuck, then translate to Ook!.

Base area (absolute cells):
  0 SENT   always 0: left sentinel for the digit walk
  1 c      input character
  2 t      loop condition temp
  3 u      copy helper
  4 n      the counter N
  5 z1     scratch / final "did we print anything" flag
  6 z2     scratch
  7 f      flag

Digit groups, stride 10, group i based at 10+10i, least significant first:
  +0 M  marker (1 = position in use)     +5 R  remainder / print-started flag
  +1 A  a's digit                        +6 K  countdown 10-R
  +2 B  b's digit                        +7 T  copy temp
  +3 I  carry into this position         +8 U  copy temp
  +4 S  sum accumulator                  +9 F  flag
"""

class BF:
    def __init__(self):
        self.out = []
        self.pos = 0

    def e(self, s):
        self.out.append(s)
        return self

    def to(self, off):
        d = off - self.pos
        self.e('>' * d if d > 0 else '<' * -d)
        self.pos = off
        return self

    def at(self, off, s):
        self.to(off)
        return self.e(s)

    def code(self):
        return ''.join(self.out)

M, A, B, I, S, R, K, T, U, F = range(10)
SENT, c, t, u, n, z1, z2, f = range(8)
G0 = 10          # group 0 base
STRIDE = 10

b = BF()

# ---------------------------------------------------------------- prompt "N? "
# z1 = 10, multiply into z2: 78 = 10*7 + 8
b.at(z1, '+' * 10)
b.e('[').at(z2, '+' * 7).at(z1, '-').e(']')
b.at(z2, '+' * 8 + '.')          # 78 'N'
b.e('-' * 15 + '.')              # 63 '?'
b.e('-' * 31 + '.')              # 32 ' '
b.e('[-]')                       # z2 = 0

# --------------------------------------------------------------- read N
b.at(c, ',')
# t = c, u = c ; then u back into c ; t -= 10
b.e('[').at(t, '+').at(u, '+').at(c, '-').e(']')
b.at(u, '[').at(c, '+').at(u, '-').e(']')
b.at(t, '-' * 10)
b.e('[')                          # while c != '\n'
b.at(c, '-' * 48)                 #   c = digit value
b.at(n, '[').at(z1, '+').at(n, '-').e(']')          # z1 = n, n = 0
b.at(z1, '[').at(n, '+' * 10).at(z1, '-').e(']')    # n = 10 * z1
b.at(c, '[').at(n, '+').at(c, '-').e(']')           # n += digit
b.at(c, ',')                      #   next char
b.at(t, '[-]')
b.at(c, '[').at(t, '+').at(u, '+').at(c, '-').e(']')
b.at(u, '[').at(c, '+').at(u, '-').e(']')
b.at(t, '-' * 10)
b.e(']')

# ------------------------------------------------- a = 0, b = 1 in group 0
b.at(G0 + M, '+')
b.at(G0 + B, '+')

# ------------------------------------------------------------- fib loop
b.at(n, '[')                      # while n
b.to(G0 + M)
b.pos = M                         # from here, offsets are relative to a group base
b.e('[')                          #   while marker: one digit position
b.at(I, '[').at(S, '+').at(I, '-').e(']')                    # S = I
b.at(A, '[').at(S, '+').at(A, '-').e(']')                    # S += A
b.at(B, '[').at(S, '+').at(A, '+').at(B, '-').e(']')         # S += B, A = old B
b.at(K, '+' * 10)
b.at(S, '[')                      #     split S into R (mod 10) and a carry
b.e('-')
b.at(R, '+')
b.at(K, '-')
b.e('[').at(T, '+').at(U, '+').at(K, '-').e(']')             # T = U = K
b.at(U, '[').at(K, '+').at(U, '-').e(']')                    # K restored
b.at(F, '+')                                                  # F = 1
b.at(T, '[').at(F, '-').at(T, '[-]').e(']')                  # F = 0 unless K == 0
b.at(F, '[')                      #       carry out
b.at(STRIDE + I, '+')             #         next position's carry in
b.at(R, '[-]')
b.at(K, '+' * 10)
b.at(F, '-')
b.e(']')
b.to(S)
b.e(']')
b.at(R, '[').at(B, '+').at(R, '-').e(']')                    # B = R
b.at(K, '[-]')
b.to(STRIDE + M)
b.pos = M                         # next group, same relative frame
b.e(']')
# pointer sits on the first unused marker; its I holds the carry out
b.at(I, '[').at(M, '+').at(B, '+').at(I, '-').e(']')
b.to(M - STRIDE)
b.pos = M
b.e('[' + '<' * STRIDE + ']')     # walk left to the sentinel
b.e('>' * STRIDE)                 # back to group 0
b.pos = G0 + M
b.at(n, '-')
b.e(']')

# ------------------------------------------------------------- print a
b.to(G0 + M)
b.pos = M
b.e('[' + '>' * STRIDE + ']')     # walk right past the most significant digit
b.e('<' * STRIDE)
b.e('[')                          # walk left, printing
b.at(A, '[').at(T, '+').at(U, '+').at(A, '-').e(']')         # T = U = A
b.at(U, '[').at(A, '+').at(U, '-').e(']')                    # A restored
b.at(T, '[').at(R, '[-]+').at(T, '[-]').e(']')               # A != 0 -> R = 1
b.at(R, '[').at(T, '+').at(U, '+').at(R, '-').e(']')         # T = U = R
b.at(U, '[').at(R, '+').at(U, '-').e(']')                    # R restored
b.at(T, '[').at(A, '+' * 48 + '.').at(T, '-').e(']')         # printing? print A
b.at(R, '[').at(R - STRIDE, '+').at(R, '-').e(']')           # carry the flag left
b.to(M - STRIDE)
b.pos = M
b.e(']')

# --------------------------------- nothing printed at all means a was zero
b.pos = SENT
b.at(f, '+')
b.at(z1, '[').at(f, '-').at(z1, '[-]').e(']')
b.at(f, '[').at(z2, '+' * 48 + '.' + '[-]').at(f, '-').e(']')
# ------------------------------------------------------------- newline
b.at(z2, '+' * 10 + '.' + '[-]')

bf = b.code()
open('/tmp/ookdev/fib.bf', 'w').write(bf + '\n')

OOK = {'>': 'Ook. Ook?', '<': 'Ook? Ook.', '+': 'Ook. Ook.', '-': 'Ook! Ook!',
       ',': 'Ook. Ook!', '.': 'Ook! Ook.', '[': 'Ook! Ook?', ']': 'Ook? Ook!'}
words = [OOK[ch] for ch in bf]
lines, cur = [], ''
for w in words:
    if len(cur) + len(w) + 1 > 72:
        lines.append(cur)
        cur = w
    else:
        cur = w if not cur else cur + ' ' + w
lines.append(cur)
open('/tmp/ookdev/fib.ook', 'w').write('\n'.join(lines) + '\n')

print('bf chars :', len(bf))
print('brackets :', bf.count('['), bf.count(']'))
print('ook pairs:', len(words), '| ook lines:', len(lines))
