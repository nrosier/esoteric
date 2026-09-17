# Befunge-93

Source code is a 2D grid. There's no "next instruction" — there's an
instruction pointer (IP) sitting on some cell, facing a direction, and
whatever character it's standing on right now is the instruction. `>` `<`
`^` `v` turn it; everything else is arithmetic, stack juggling, or I/O; and
the grid wraps like a torus, so falling off one edge puts you back on the
opposite one. There is no `if`, no `while`, no function, no variable name —
just a pointer wandering a plane, and control flow is *literally* the shape
you draw.

Befunge-93 also has no comment syntax (there's no character that means
"ignore the rest of this"), so — same house rule as everywhere else in this
repo — the explanation lives here instead.

## The grid

The classic Befunge-93 grid is a fixed **80 columns × 25 rows**. Not "80 by
default" — 80, full stop, in every conforming interpreter, including the one
used here. Confirmed empirically by binary search: a program with something
useful at column 79 runs fine; the exact same thing shifted one column to
column 80 makes that row silently wrap back to column 0, and the row loops
forever instead of erroring. Rows behave the same way at row 25. Nothing
tells you this happened — the IP just keeps circling — which makes it a nasty
thing to debug the first time and a very easy thing to design around once you
know it's there.

Fibonacci.bf's control-flow spine is wide enough that it can't fit on one row
without hitting that ceiling (see "the elevator" below).

## The stack, and the loop idiom

Befunge has one data stack. `1 2 3` as source pushes 1, then 2, then 3 (top
of stack is 3). `+` pops two and pushes their sum. `:` duplicates the top.
`\` swaps the top two. `!` pops and pushes the logical NOT (0 → 1, anything
else → 0). `p` and `g` read and write a cell of the *grid itself* — push
`value x y` then `p` to store, push `x y` then `g` to fetch — which is how
Befunge does "variables": named cells off in blank space that the running
program uses as scratch memory.

Every loop in both programs here is built from the same three-row shape:

```
check row:     >  [test]  !  |
body row:          [work]           v
corridor row:   ^ ------------------ <
```

The IP enters the check row moving right, runs `[test]`, and `!` flips it
(0 → 1 means "still true", note the double negative). `|` is the vertical
branch: it pops one value and sends the IP up on nonzero, down on zero. So
"the loop continues" and "the loop is done" are just *up* versus *down* out
of the same `|` — down drops into the body row below, which does the real
work and then turns down into the corridor, which carries the IP back left
and up into the check row for another pass. Up out of `|`, by contrast,
escapes into whatever sits directly above the check row — which is wherever
the *next* phase of the program happens to be.

`Fibonacci.bf` chains three of these: accumulate `fib(n)` into `a`, split `a`
into decimal digits, then print the digits back out most-significant-first.

## `HelloWorld.bf`

```
"!dlroW ,olleH">:#,_25*,@
```

`"..."` is Befunge's *string mode*: while inside quotes, every character
gets pushed onto the stack as its ASCII value instead of being executed —
which is why the greeting is spelled backwards. Stack order is
last-pushed-is-on-top, and it's about to get popped off top-first, so
pushing it back-to-front is what makes it come out forwards.

After the closing `"`, five cells — `>` `:` `#` `,` `_` — form a loop the IP
walks back and forth over, not just forward through. Moving *right*: `>`
(go right), `:` (duplicate the top of stack), `#` (trampoline — skip the very
next cell without executing it, here jumping clean over the `,`), landing on
`_`, which pops the just-made duplicate and branches: nonzero → left,
zero → right. For an actual character this is nonzero, so the IP heads back
*left* — and going left, it's no longer skipping anything, so it walks
straight onto the `,` it jumped over a moment ago and prints the *other*
copy (the original, still sitting under where the duplicate was). It keeps
going left over `#` — trampolining again, this time skipping `:` — lands on
`>`, faces right again, and the cycle repeats on the next character. Test
and print are the two duplicates of the same value; the trampoline's whole
job is making sure only the *leftward* pass ever reaches the print cell.

Fourteen pushed characters, fourteen cycles... except there are only 13 (the
string is 13 characters — string mode itself contributes nothing to print).
After the last one, the loop tries to dup an empty stack, which most
Befunge implementations (and this one) treat as an implicit 0. `_` pops that
0, and zero branches *right* this time — straight past the `,` for good,
into `25*,@`: push 2, push 5, multiply (10, i.e. `\n`), print it, halt. The
loop terminates by running out of stack, not by counting anything.

## `Fibonacci.bf`

`generate.py` is the actual program; it's a Python assembler that lays out
characters on an 80×25 grid and writes the result to `Fibonacci.bf`. Nobody
free-hands two-dimensional Befunge layouts with named offsets by counting
columns manually — this is where the design lives, commented, and
`Fibonacci.bf` is its (checked-in) output. Regenerating is the regression
test:

```bash
python3 generate.py && git diff --exit-code Fibonacci.bf
```

Grid storage holds five values via `p`/`g`, all on row `y=9`: `a` at x=0,
`b` at x=1, `n` at x=2, a digit-extraction scratch `printV` at x=3, and a
digit count at x=4.

**Phase 1 — accumulate.** Read `n` from stdin (`&`), print `"N? "`, seed
`a=0, b=1`. While `n>0`: `a, b = b, a+b`, `n -= 1`. Standard iterative
Fibonacci, just written as a check/body/corridor loop instead of a `while`.

**Phase 2 — extract digits.** `a` is a single number; printing it means
peeling off decimal digits, and there's no `a` until it's fully computed, so
this can't start until phase 1's loop exits. It's a *do-while*, not a
pre-checked loop (every number has at least one digit, even 0):
`digit = printV % 10`, `printV /= 10`, `count += 1`, stop once `printV` hits
0. Digits land on the stack in least-significant-first order (that's the
order they were extracted in).

**The elevator.** Phase 2's "done" branch lands back on row 0, close to
column 75. Phase 3 (printing) needs about 20 more columns of check/body/
corridor to itself — enough to blow through column 80. Rather than let row 0
keep growing rightward into the wraparound bug described above, the "done"
landing turns the IP *right* into blank space, then *down* through two
entirely blank rows, then *left* along a third blank row back to a small
column number, then *down* again into fresh rows. Four turns just to move
the story to a part of the grid with room left. It's not clever, it's a
detour — but it's a detour that never touches a column above 80.

**Phase 3 — print back.** Another do-while, popping digits off the stack
(now most-significant-first, since they went on least-significant-first):
`print(digit + '0')`, `count -= 1`, stop at 0. Finishes with a `\n` and `@`
(halt).

## Known warts

- **Grid storage is 8-bit and *signed*.** This is the one that actually
  limits the program. Befunge-93's `p`/`g` cells are one byte each, and this
  interpreter treats that byte as *signed* (range −128…127) rather than
  unsigned. The data *stack* isn't limited this way — pure stack arithmetic
  holds at least 200 correctly — but the moment a value round-trips through
  `p`/`g` storage, anything ≥128 wraps: 200 stored and fetched comes back as
  −56 (200 mod 256, reinterpreted as a signed byte), 144 comes back as −112,
  and so on. `a` and `b` live in `p`/`g` storage between iterations, so
  `fib(12) = 144` is the first value this breaks. Confirmed with isolated
  push/store/fetch/print tests: a value pushed and printed straight off the
  stack comes out correct; the identical value stored via `p` and fetched
  back via `g` comes out wrapped.
  **Practical effect: `Fibonacci.bf` is correct for `n = 0` through `n = 11`**
  (`fib(11) = 89` is the largest Fibonacci number under 128) **and wraps for
  `n ≥ 12`.** A negative, wrapped `a` doesn't just print wrong — the
  wrong digits genuinely garble into punctuation, because C-style truncating
  `%`/`/` on a negative dividend produces negative "digits", and
  `digit + '0'` maps a negative digit to whatever ASCII character sits below
  `'0'`. `n=20` was seen to print `109` instead of `6765`; earlier debugging
  saw fragments like `//.` and `.-` for the intermediate corrupted values.
  Fixing this properly means never storing `a`/`b` in `p`/`g` at all — keeping
  the running pair entirely on the stack, Ook!'s digit-array approach
  translated to Befunge, or similar — and was judged out of scope here: a
  clean 2-variable rotation `(a,b) → (b,a+b)` needs something like Forth's
  `OVER`, which doesn't fall out of Befunge's only two stack primitives,
  `:` (dup) and `\` (swap), the same way it doesn't fall out of `DUP`+`SWAP`
  alone in Forth.
- **No negative-number handling.** `&` reads an int the way the interpreter's
  own parser reads it; negative input wasn't tested and Fibonacci of a
  negative index isn't a defined thing here regardless.
- **The 80×25 grid is a hard ceiling on program *size*, not on the numbers it
  computes.** A program needing more spine than that has to fold back on
  itself (see "the elevator") rather than simply writing a wider grid — this
  interpreter does not support Befunge-98's unbounded grid.

## Running it

Both files are plain text; there's no build step. `bef` reads a `.bf` file
and runs it directly.

### macOS (tested)

```bash
brew install befunge93
cd Befunge

bef -q HelloWorld.bf
# -> Hello, World!

echo 10 | bef -q Fibonacci.bf
# -> N? 55
```

`brew install befunge93` links `bef` straight onto `PATH` — no `venv`, no
`export`, unlike some of the other interpreters in this repo.

### Linux (upstream route, not run here)

`befunge93` is a Homebrew **core** formula (the same one used above), and
Homebrew on Linux ("Linuxbrew") builds core formulae the same way it does on
macOS:

```bash
brew install befunge93
cd Befunge
echo 10 | bef -q Fibonacci.bf
```

If Homebrew isn't set up, the formula's own upstream is
[catseye.tc's reference `befunge93`](https://catseye.tc/article/Languages.md#befunge-93),
buildable from source with a C compiler — not attempted here.

### Windows (upstream route, not run here)

No native Windows build is documented for this interpreter. Use WSL and
follow the Linux route above:

```powershell
wsl
brew install befunge93
cd Befunge
echo 10 | bef -q Fibonacci.bf
```

### What was actually tested

| | Version | Result |
|---|---|---|
| macOS | 26.6.2 (25G83) | ✅ everything in this README |
| `befunge93` (`bef`) | 2.25 | ✅ `HelloWorld.bf`, byte-exact (`Hello, World!\n`, 14 bytes via `od -c`); `Fibonacci.bf` for `n = 0…11`, all exact; `n ≥ 12` confirmed to wrap, as documented above |
| CPython | 3.14.7 | ✅ `generate.py` reproduces the committed `Fibonacci.bf` byte for byte |
| Linux | — | ❌ not run; same `brew install befunge93`, same binary formula |
| Windows | — | ❌ not run; WSL route above is this repo's usual escape hatch, adapted |

## Files in this folder

| File | What it is |
|---|---|
| `HelloWorld.bf` | **a program** — the string-mode print loop |
| `Fibonacci.bf` | **the program** — three chained loops and one detour around the grid's column limit |
| `generate.py` | the assembler that lays `Fibonacci.bf` out on the grid, with the named offsets and reasoning Befunge itself has no syntax for |
