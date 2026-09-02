#!/usr/bin/env python3
"""Translate Ook! into Brainfuck.

Ook! is Brainfuck with the eight instructions spelled out in pairs of three
words, so the translation is a lookup table and nothing else.

    python3 ook2bf.py Fibonacci.ook > Fibonacci.bf
    python3 ook2bf.py Fibonacci.ook Fibonacci.bf

Line breaks between Ook pairs are insignificant. Anything that is not an Ook
word is an error rather than something to skip quietly: Ook! has no comment
syntax, so stray text is a typo, not a note.
"""

import re
import sys

OOK = {
    ('.', '?'): '>', ('?', '.'): '<',
    ('.', '.'): '+', ('!', '!'): '-',
    ('.', '!'): ',', ('!', '.'): '.',
    ('!', '?'): '[', ('?', '!'): ']',
}

WORD = re.compile(r'Ook([.?!])')


def translate(text):
    words = text.split()
    for i, word in enumerate(words, 1):
        if not WORD.fullmatch(word):
            raise SystemExit(f'word {i} is {word!r}, which is not an Ook')
    if len(words) % 2:
        raise SystemExit(f'{len(words)} Ooks: an odd Ook is half an instruction')

    marks = [WORD.fullmatch(w)[1] for w in words]
    out = []
    for i in range(0, len(marks), 2):
        pair = (marks[i], marks[i + 1])
        if pair == ('?', '?'):
            raise SystemExit(f'Ook? Ook? at pair {i // 2 + 1}: the Memory '
                             'Pointer wants a banana, and this translator '
                             'does not carry fruit')
        out.append(OOK[pair])
    return ''.join(out)


def main(argv):
    if not 2 <= len(argv) <= 3:
        raise SystemExit(f'usage: {argv[0]} IN.ook [OUT.bf]')
    with open(argv[1]) as fh:
        code = translate(fh.read())
    if len(argv) == 3:
        with open(argv[2], 'w') as fh:
            fh.write(code + '\n')
    else:
        print(code)


if __name__ == '__main__':
    main(sys.argv)
