import sys
src = open(sys.argv[1]).read()
code = [c for c in src if c in '><+-.,[]']
jump = {}
st = []
for i, c in enumerate(code):
    if c == '[': st.append(i)
    elif c == ']': j = st.pop(); jump[i] = j; jump[j] = i
inp = (sys.argv[2] + '\n').encode() if len(sys.argv) > 2 else b''
ii = 0
tape = [0] * 400
p = ip = steps = 0
out = []
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20_000_000
while ip < len(code) and steps < limit:
    c = code[ip]; steps += 1
    if c == '>': p += 1
    elif c == '<': p -= 1
    elif c == '+': tape[p] = (tape[p] + 1) % 256
    elif c == '-': tape[p] = (tape[p] - 1) % 256
    elif c == '.': out.append(tape[p])
    elif c == ',':
        tape[p] = inp[ii] if ii < len(inp) else 0; ii += 1
    elif c == '[':
        if tape[p] == 0: ip = jump[ip]
    elif c == ']':
        if tape[p] != 0: ip = jump[ip]
    ip += 1
print('out :', bytes(out).decode('latin1').rstrip('\n') + ('' if out else '<none>'))
print('steps:', steps, '| halted:', ip >= len(code), '| ptr:', p)
print('base :', tape[:10])
for g in range(0, 6):
    b = 10 + 10 * g
    if any(tape[b:b+10]): print(f'g{g}  :', tape[b:b+10])
