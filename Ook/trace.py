#!/usr/bin/env python3
"""Run an Ook! or Brainfuck program and dump the tape afterwards.

A debugging aid for poking at Fibonacci.ook, not the proof that it works —
that is bfi's job (see README.md). What this adds is a view of the digit
groups, which is the only way the algorithm is legible at all:

    python3 trace.py Fibonacci.ook 10
    python3 trace.py Fibonacci.bf 90 --steps 5000000

Cells wrap at 256, exactly like bfi's, so a run here and a run there agree.
"""

import sys

import ook2bf

BASE = ('SENT', 'c', 't', 'u', 'n', 'z1', 'z2', 'f')
GROUP = ('M', 'A', 'B', 'I', 'S', 'R', 'K', 'T', 'U', 'F')
G0, STRIDE = 10, 10


def run(code, stdin, tape_size=30000, limit=200_000_000):
    code = [ch for ch in code if ch in '><+-.,[]']
    jump, stack = {}, []
    for i, ch in enumerate(code):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            start = stack.pop()
            jump[start], jump[i] = i, start
    if stack:
        raise SystemExit('unmatched Ook! Ook?')

    tape = [0] * tape_size
    out, data = [], iter(stdin)
    ptr = ip = steps = 0
    while ip < len(code) and steps < limit:
        ch = code[ip]
        steps += 1
        if ch == '>':
            ptr += 1
        elif ch == '<':
            ptr -= 1
        elif ch == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif ch == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif ch == '.':
            out.append(tape[ptr])
        elif ch == ',':
            tape[ptr] = next(data, 0)
        elif ch == '[' and tape[ptr] == 0:
            ip = jump[ip]
        elif ch == ']' and tape[ptr] != 0:
            ip = jump[ip]
        ip += 1
    return bytes(out), tape, steps, ip >= len(code)


def main(argv):
    if not 2 <= len(argv) <= 5:
        raise SystemExit(f'usage: {argv[0]} PROGRAM [INPUT] [--steps N]')
    args = [a for a in argv[1:] if not a.startswith('--')]
    limit = 200_000_000
    for a in argv[1:]:
        if a.startswith('--steps='):
            limit = int(a.split('=', 1)[1])

    text = open(args[0]).read()
    code = ook2bf.translate(text) if 'Ook' in text else text
    stdin = (args[1] + '\n').encode() if len(args) > 1 else b''

    out, tape, steps, halted = run(code, stdin, limit=limit)
    print('output:', out.decode('latin-1').replace('\n', '\\n'))
    print(f'steps : {steps:,}{"" if halted else "  (LIMIT REACHED, still running)"}')
    print('base  :', ' '.join(f'{n}={v}' for n, v in zip(BASE, tape) if v))
    for g in range((len(tape) - G0) // STRIDE):
        cells = tape[G0 + g * STRIDE:G0 + (g + 1) * STRIDE]
        if not any(cells):
            break
        print(f'digit {g}:', ' '.join(f'{n}={v}' for n, v in zip(GROUP, cells) if v))


if __name__ == '__main__':
    main(sys.argv)
