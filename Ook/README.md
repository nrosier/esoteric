# Ook!

> **Design Principles**
> A programming language should be writable and readable by orang-utans.
> To this end, the syntax should be simple, easy to remember, and not mention
> the word "monkey".
> Bananas are good.
>
> — David Morgan-Mar, [the Ook! specification](https://www.dangermouse.net/esoteric/ook.html)

Ook! is Brainfuck with the punctuation spelled out loud. Same tape, same eight
instructions, same total absence of anything resembling a number — but instead
of `>` you write `Ook. Ook?`, and instead of a compact wall of symbols you get
9,640 bytes of ape.

The language has no comments, on the grounds that "the word 'ook' can convey
entire ideas, emotions, and abstract thoughts depending on the nuances of
inflection". This README is that inflection.

## The whole language

Three words — `Ook.`, `Ook?`, `Ook!` — combined into pairs. Nine pairs exist,
eight of them do something:

| Ook! | Brainfuck | Meaning |
|---|---|---|
| `Ook. Ook?` | `>` | Move the Memory Pointer to the next cell |
| `Ook? Ook.` | `<` | Move the Memory Pointer to the previous cell |
| `Ook. Ook.` | `+` | Increment the cell under the pointer |
| `Ook! Ook!` | `-` | Decrement the cell under the pointer |
| `Ook. Ook!` | `,` | Read a character from stdin, store its ASCII value |
| `Ook! Ook.` | `.` | Print the character whose ASCII value is in the cell |
| `Ook! Ook?` | `[` | If the cell is zero, jump past the matching `Ook? Ook!` |
| `Ook? Ook!` | `]` | If the cell is non-zero, jump back to the matching `Ook! Ook?` |
| `Ook? Ook?` | — | **Give the Memory Pointer a banana.** |

Programs must contain an even number of Ooks. Line breaks are ignored. That is
the entire specification, banana included.

`Fibonacci.ook` is 964 instructions — 1,928 Ooks over 138 lines:

| | `>` | `<` | `+` | `-` | `[` | `]` | `.` | `,` | banana |
|---|---|---|---|---|---|---|---|---|---|
| count | 236 | 230 | 201 | 173 | 58 | 58 | 6 | 2 | 0 |

Two reads, six prints, and 466 instructions whose entire job is moving the
pointer somewhere else. That ratio is the honest summary of programming in this
family of languages.

## Why Fibonacci is hard here, and why this program is 964 instructions

The naive version is about thirty instructions: keep `a` and `b` in two cells
and add one into the other `n` times. It is also useless, for two independent
reasons.

**Arithmetic is unary.** `[>+<-]` — the only way to add — moves one unit per
iteration, so adding `b` to `a` takes `b` steps. Not `log b`. Not a constant.
`b` steps. Computing `fib(50)` that way costs about 3 × 10¹⁰ unit moves;
`fib(100)` costs 9 × 10²⁰, which is a couple of thousand times more than there
have been seconds since the Big Bang.

**Cells are bytes in practice.** The spec says "a large array of integers", and
one interpreter really does give you unbounded integers — but every interpreter
anyone actually installs wraps at 256. `fib(13) = 233` fits; `fib(14) = 377`
does not.

Both problems have the same fix: **stop storing numbers in cells.** Store them
as decimal digit arrays, one digit per group of cells, least significant first.
Then

- no cell ever exceeds 255, so byte cells and bignum cells behave identically;
- a Fibonacci step costs one pass over the digits instead of `fib(n)` unit
  moves, so the whole thing is polynomial and the answer comes back instantly.

The result is exact to `fib(255) = 87571595343018854458033386304178158174356588264390370`
in half a second, on an interpreter whose cells cannot count past 255. That
gap between what the machine can hold and what the program can compute is the
entire point of the exercise.

## The tape

Cell 0 is never used for data. It stays zero forever so that the digit walk has
something to stop against — the only way to find "the beginning of the array"
when you don't know how far right you have wandered.

| Cell | Name | Holds |
|---|---|---|
| 0 | `SENT` | permanently zero: the left sentinel |
| 1 | `c` | the character just read |
| 2 | `t` | loop condition for the input parser |
| 3 | `u` | copy scratch |
| 4 | `n` | the counter, counted down to zero |
| 5 | `z1` | scratch, then "did we print anything" |
| 6 | `z2` | scratch |
| 7 | `f` | flag for the is-zero tests |

From cell 10 onwards the tape is digit groups, ten cells each, digit *i* at
`10 + 10i`, least significant digit first:

| Offset | Name | Holds |
|---|---|---|
| +0 | `M` | marker: 1 if this digit position exists |
| +1 | `A` | this digit of `a` |
| +2 | `B` | this digit of `b` |
| +3 | `I` | carry coming into this position |
| +4 | `S` | sum accumulator |
| +5 | `R` | remainder, later reused as the print flag |
| +6 | `K` | countdown from 10 |
| +7 | `T` | copy scratch |
| +8 | `U` | copy scratch |
| +9 | `F` | flag |

The marker is what makes a variable-length array possible. `Ook! Ook?` followed
by ten `Ook. Ook?`s and `Ook? Ook!` — `[>>>>>>>>>>]` — walks right over groups
until it lands on a zero marker, i.e. one past the end of the number. The same
loop with `<` walks back until it hits cell 0. Neither loop knows how many
digits there are, which is exactly the point: `fib(255)` has 54 of them and the
program was never told.

## One Fibonacci step

`a, b = b, a + b`, digit by digit, in a single left-to-right pass:

```
S ← I + A + B          carry in, a's digit, b's digit
A ← old B              (falls out of the same move loop, for free)
B ← S mod 10
I of the next group ← S div 10
```

The swap needs no temporary. Moving `B` into `S` can deposit a second copy in
`A` on the way past, and `A`'s old value is already gone into `S`:

```python
b.at(I, '[').at(S, '+').at(I, '-').e(']')                # S = I
b.at(A, '[').at(S, '+').at(A, '-').e(']')                # S += A
b.at(B, '[').at(S, '+').at(A, '+').at(B, '-').e(']')     # S += B, and A = old B
```

Then `S ≤ 9 + 9 + 1 = 19` has to be split into a digit and a carry — and
Brainfuck has no comparison, no division, no way to ask "is this bigger than
ten". It can only ask *"is this cell zero?"*, and only by destroying the cell.

So the split counts. `K` starts at 10; every unit taken out of `S` adds one to
`R` and takes one off `K`. If `K` reaches zero we have moved exactly ten, so:
bump the *next* group's carry, reset `R` to 0, put `K` back to 10. When `S` is
empty, `R` is `S mod 10` and the carry is already sitting where the next
iteration expects it. Because `S ≤ 19`, `K` can hit zero at most once, so the
carry is always 0 or 1.

Testing `K` for zero without destroying it is the standard three-cell dance —
copy it, wreck the copy, and let a flag survive:

```python
b.e('[').at(T, '+').at(U, '+').at(K, '-').e(']')   # T = U = K, K = 0
b.at(U, '[').at(K, '+').at(U, '-').e(']')          # K restored from U
b.at(F, '+')                                        # assume zero
b.at(T, '[').at(F, '-').at(T, '[-]').e(']')        # wrong if the copy is non-zero
b.at(F, '[')                                        # ... and here is the carry
```

That gadget runs once per unit of every digit of every step. It is the reason
`n = 255` costs 9.2 million instructions instead of nine thousand, and it is
also the reason the program works at all.

**Growing a digit.** When the pass ends, the pointer is sitting on the first
zero marker — one past the top digit — and a carry off the end is already in
that group's `I`. Setting `M` and `B` from it extends the number by one digit:
`b` gains a digit exactly when `a + b` does, and `a`'s digit there is 0, which
is already the case. No reallocation, no length variable.

## Printing, and the leading zero

`a` and `b` share one array, sized to `b`, so `a` has a leading zero whenever
it is a digit shorter — which is most of the time. Printing walks right to the
end, steps back onto the top digit, then walks left emitting `digit + 48`.

A flag in each group (`R`, free again by then) says whether printing has
started; it is set by any non-zero digit, and moved one group left at each step.
Leading zeros therefore print nothing, and everything after the first real digit
prints unconditionally.

The flag falls off the left end into cell 5, so after the walk the program can
ask one last question: *did anything get printed at all?* If not, `a` was zero
— the `n = 0` case — and it prints `0` explicitly. That check exists for
exactly one input, and without it `echo 0` would print `N? ` and stop.

## Running it

Ook! interpreters are, without exception, broken (see [the interpreter
zoo](#the-interpreter-zoo) below — this is not an exaggeration). The practical
route is the one the language's own isomorphism suggests: translate to
Brainfuck and run that. `ook2bf.py` does the translation, `bfi` runs it, and
both work identically on all three platforms because both are pure Python.

`Fibonacci.bf` is committed alongside `Fibonacci.ook`, so you can skip the
translation step if you only want the answer — but the `.ook` file is the
program, and `python3 ook2bf.py Fibonacci.ook` regenerates the `.bf` byte for
byte.

### macOS (tested)

```bash
cd Ook
python3 -m venv .venv
source .venv/bin/activate
pip install bfi

python3 ook2bf.py Fibonacci.ook Fibonacci.bf   # optional: it is committed
echo 10 | bfi Fibonacci.bf                     # -> N? 55
```

Or interactively, which is how the prompt is meant to be seen:

```bash
bfi Fibonacci.bf
N? 12
144
```

### Linux (upstream route, not run here)

Identical — `bfi` is pure Python with no dependencies. On a distro that ships
Python without `venv`, install `python3-venv` first:

```bash
sudo apt install python3-venv     # Debian/Ubuntu only if `python3 -m venv` fails
cd Ook
python3 -m venv .venv && source .venv/bin/activate
pip install bfi
echo 10 | bfi Fibonacci.bf
```

### Windows (upstream route, not run here)

PowerShell:

```powershell
cd Ook
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install bfi

"10" | bfi Fibonacci.bf
```

`cmd.exe`:

```bat
cd Ook
py -m venv .venv
.venv\Scripts\activate.bat
pip install bfi

echo 10| bfi Fibonacci.bf
```

Two Windows-specific notes, both real:

- **`echo 10| bfi` — no space before the pipe.** `cmd.exe` includes any space
  you put there in the piped text, and a space (32) is not a digit, so
  `echo 10 | bfi` asks for a Fibonacci number nobody ordered.
- **Carriage returns are handled.** Windows pipes send `10\r\n`, and the parser
  stops on `\r` as well as `\n`. This was worth 20 instructions: without it,
  `echo 10` on Windows means `n = 65`, because `13 - 48` wraps to 221 and the
  parser cheerfully multiplies it in. The guard costs 160 of the program's 964
  instructions — a sixth of the whole thing, spent on Windows. Verified on macOS
  with `printf '10\r\n'`, which gives the same 55 as `printf '10\n'`.

### What was actually tested

| | Version | Result |
|---|---|---|
| macOS | 26.6.2 (25G83) | ✅ every case in this README |
| CPython | 3.14.7 | ✅ `ook2bf.py`, `generate.py`, `trace.py` |
| `bfi` | 1.1.1 | ✅ `n = 0…60` plus 90, 100, 128, 200, 255, all exact against Python |
| Linux | — | ❌ not run; same pip route, pure Python |
| Windows | — | ❌ not run; commands above are upstream's, adapted |

The `n = 0…60` sweep compares `bfi`'s output byte for byte against Python's own
Fibonacci, including the `N? ` prompt and the trailing newline. Timings on this
machine: `n = 10` 0.06 s (18,727 instructions executed), `n = 100` 0.13 s
(1,413,401), `n = 255` 0.51 s (9,198,473).

## The interpreter zoo

Ook! has been implemented many times and, as far as this folder can determine,
never twice compatibly. Every implementation reachable through a package
manager is broken in some way that matters for a program that reads input:

| Implementation | Route | Verdict |
|---|---|---|
| **`bfi` 1.1.1** (Brainfuck) | `pip install bfi` | ✅ **tested, correct.** `,` is `ord(os.read(0, 1))`, one byte at a time; output flushed per byte, so the prompt appears before the read; 8-bit wrapping cells; 30,000-cell tape (`--size` to grow it) |
| `brainfuck` 2.7.3 (Brainfuck) | `brew install brainfuck` | ❌ **tested, broken input.** `,.,.,.` fed `abc` prints `aaa` — every read returns the *first* character forever, so the parse loop never sees a newline and hangs |
| `esolangs` 0.1.0 | `pip install esolangs` | ❌ **tested, broken input.** `,` consumes a whole *line* and returns its first character, then raises `EOFError`. Sixty-odd Brainfuck relatives, no Ook! |
| `ook.js` 1.0.2 | `npm i ook.js` | ❌ **source read, not run.** Prints with `console.log`, so every output character gets its own newline; input goes through `rl.question`, whose callback fires after the interpreter loop has already finished; and `source.split(" ")` cannot cope with line breaks |
| `Language::Ook` 0.03 | CPAN | ❌ **source read, not run.** Its `,` is `read(STDIN,$cell[$ptr],1)?ord($cell[$ptr]):0` — the `ord` result is discarded and the cell keeps the *character*, so the tape holds strings and `+` does Perl's magic increment |
| `pook.py` (Grønnesby) | linked from the spec | ⚠️ **source read, not run.** The only implementation found with both correct `,` and genuinely unbounded integer cells, i.e. the spec's actual memory model. Python 2 only (`print` statement, string exceptions), no license file, and it rescans the whole program to find each matching bracket — so it is also the slowest possible way to run 9 million instructions |
| `brainook` 0.3.0 | `npm i -g brainook` | ⬜ not run here. An MIT-licensed Ook!↔Brainfuck translator, if you would rather not use `ook2bf.py` |

Two honest consequences of that table:

1. **`Fibonacci.ook` has never been executed by an Ook! interpreter** — only by
   a Brainfuck interpreter after a 1:1 token substitution. Since Ook! *is*
   Brainfuck with different spellings, and since `ook2bf.py` round-trips the
   file byte for byte, this is the same program. It is still worth saying out
   loud.
2. The spec's "array of integers" is theoretical. Everything installable gives
   you bytes, which is why this program was written to need nothing wider.

## Known warts

- **`N` itself lives in one cell, so `N ≤ 255`.** Verified: `n = 255` gives the
  correct 54-digit answer, `n = 256` prints `0` (it wrapped to `fib(0)`), and
  `n = 300` prints `701408733`, which is `fib(44)`. The *result* is unbounded;
  only the counter is a byte. On an interpreter with the spec's integer cells,
  this limit disappears untouched.
- **Missing trailing newline crashes `bfi`.** `printf '10' | bfi Fibonacci.bf`
  dies with `TypeError: ord() expected a character, but string of length 0
  found` — `bfi` raises at EOF rather than returning 0, and the parser is still
  waiting for its terminator. `echo`, `printf '10\n'` and typing at the prompt
  are all fine. Empty stdin fails the same way, after printing `N? `.
- **Non-digits are read as digits.** Anything other than `\n` or `\r` is
  treated as a digit and `c - 48` is allowed to wrap: `echo abc` computes
  `n = 75` and prints `fib(75) = 2111485077978050` with a completely straight
  face. Leading zeros are harmless (`echo 007` → `13`).
- **No input validation is possible in any real sense.** Range checks need
  comparisons; Brainfuck has none. See the carry gadget above for what "is this
  ten yet" costs when the only question you may ask is "is this zero".
- **Negative input is not a thing.** `-` is not a digit, so `echo -3` parses as
  `n = 229` (`45 - 48` wraps to 253, then `253 × 10 + 3` wraps to 229) and
  prints all 48 digits of `fib(229)` without hesitating. The other four
  languages in this repo at least know what a minus sign is.
- **The tape needs `10 + 10 × (digits + 1)` cells.** `bfi`'s default 30,000
  covers roughly 2,990 digits, i.e. `fib(14000)`-ish — far past where the
  half-second run time stops being half a second.

## Files in this folder

| File | What it is |
|---|---|
| `Fibonacci.ook` | **the program** — 964 instructions of ape |
| `Fibonacci.bf` | the same program as Brainfuck, committed for convenience |
| `ook2bf.py` | Ook! → Brainfuck translator. Rejects odd Ook counts, non-Ook words, and bananas |
| `generate.py` | the assembler that emits both files. Nobody hand-writes 1,928 Ooks; this is where the algorithm actually lives, in named cells with comments Ook! cannot have |
| `trace.py` | debugging aid: runs either file and dumps the digit groups afterwards. Not the proof — `bfi` is |

`generate.py` is deterministic and reproduces both committed files byte for
byte, which is also the regression test:

```bash
python3 generate.py && git diff --exit-code Fibonacci.ook Fibonacci.bf
```

### The same problem, five ways

| | Shakespeare | LOLCODE | Rockstar | Chef | Ook! |
|---|---|---|---|---|---|
| Temp variable | none — swap done arithmetically | `nxt` | `the future` | none — the mixing bowl | none — the digit's own sum cell |
| Guard for `n <= 0` | explicit scene-jump guard | explicit `n < 0` guard | free (`while n > 0`) | **impossible** — no conditionals | **impossible** — no comparisons |
| Numeric type | Python ints, unbounded | signed 64-bit, wraps at `n=93` | .NET `decimal`, exact to `n=138` | Python ints, unbounded | decimal digits on a byte tape, exact to `n=255` |
| Cost of `a + b` | one line | one line | one line | one line | one pass per digit, plus a countdown per unit |
| Prompt before input | yes | yes | yes | no — output is deferred | yes |
| Reads like | a stage play | a cat | a power ballad | a fruitcake | an orang-utan |

Ook! is the only one of the five where the *language* contributes nothing to the
answer and the entire program is scaffolding. Shakespeare gives you variables
with feelings, Chef gives you stacks made of mixing bowls, Rockstar gives you
arithmetic that scans — Ook! gives you a tape, three words, and a banana.
