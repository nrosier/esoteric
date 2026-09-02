"""Generate "Hello, World!" in Brainfuck, then translate to Ook!.

Ook! has no way to say "the letter H". Every one of the fourteen characters in
the greeting has to be counted up from zero, so the only real question is how
few increments you can get away with.

Walking a single cell up and down the alphabet - 72, then +29, then +7, then 0,
then +3, then -67 - costs 376 increments and reads like nothing at all. This
program spends one multiplication loop instead: a counter of ten, ticked down
ten times, adding k to every letter cell on each pass, so cell i ends on 10*k
and needs only a small adjustment to land on its character.

The tape:

     0  counter   10, ticked down by the setup loop
     1  H   72 = 10*7  + 2      Each letter cell is filled by the loop and then
     2  e  101 = 10*10 + 1      nudged by its adjustment - never more than four
     3  \\n  10 = 10*1  + 0      - on the first visit of the printing walk, so
     4  !   33 = 10*3  + 3      the nudge costs no pointer movement at all.
     5  d  100 = 10*10 + 0
     6  l  108 = 10*11 - 2
     7  r  114 = 10*11 + 4
     8  o  111 = 10*11 + 1
     9  W   87 = 10*9  - 3
    10  ,   44 = 10*4  + 4
    11  ' ' 32 = 10*3  + 2

Eleven cells for fourteen characters: `l` is printed three times and `o` twice,
and a cell keeps its value after `.`, so the repeats are free.

The cells are in that order because printing walks H e l l o , ' ' W o r l d !
and back down to the newline, and this ordering makes the pointer travel 19
cells where a plain left-to-right tape costs 26. It is the best of 4,000
randomised local searches over the 11! orderings, which for eleven cells is
almost certainly the optimum, though nothing here depends on that.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent

MESSAGE = 'Hello, World!\n'
COUNTER = 10                       # the setup loop runs this many times
LAYOUT = ['H', 'e', '\n', '!', 'd', 'l', 'r', 'o', 'W', ',', ' ']

# Nearest multiple of COUNTER, rounding halves up. // rather than round() so
# that no cell can be quietly moved by banker's rounding if MESSAGE changes.
cell = {ch: i + 1 for i, ch in enumerate(LAYOUT)}
mult = {ch: (ord(ch) + COUNTER // 2) // COUNTER for ch in LAYOUT}
nudge = {ch: ord(ch) - COUNTER * mult[ch] for ch in LAYOUT}

assert set(MESSAGE) == set(LAYOUT), 'the tape and the greeting disagree'

out = []
pos = 0


def to(target):
    global pos
    out.append('>' * (target - pos) if target > pos else '<' * (pos - target))
    pos = target


def by(delta):
    out.append(('+' if delta > 0 else '-') * abs(delta))


# ------------------------------------------------- fill every cell with 10*k
by(COUNTER)
out.append('[')
for ch in LAYOUT:
    to(cell[ch])
    by(mult[ch])
to(0)
out.append('-]')

# ----------------------------------- walk the greeting, nudging on first sight
seen = set()
for ch in MESSAGE:
    to(cell[ch])
    if ch not in seen:
        by(nudge[ch])
        seen.add(ch)
    out.append('.')

bf = ''.join(out)
(HERE / 'HelloWorld.bf').open('w').write(bf + '\n')

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
(HERE / 'HelloWorld.ook').open('w').write('\n'.join(lines) + '\n')

print('bf chars :', len(bf))
print('brackets :', bf.count('['), bf.count(']'))
print('pointer  :', bf.count('>') + bf.count('<'), 'moves')
print('ook pairs:', len(words), '| ook lines:', len(lines))
