# Shakespeare Programming Language (SPL)

Source code is a **stage play**. It must read like Shakespeare and compile like
a program, and the two constraints fight each other constantly, which is the
point.

Designed in 2001 by Karl Hasselström and Jon Åslund as a language whose source
code "doesn't look like source code at all."

## The core conceit

| Play | Program |
|---|---|
| Title (first line, ends in `.`) | A comment. Completely ignored. |
| Dramatis personae | Variable declarations. Names must come from a fixed list of real Shakespeare characters (`Romeo`, `Juliet`, `Ophelia`, `Macbeth`, `The Ghost`, …). Their descriptions are ignored. |
| A character | A signed integer variable, plus a personal **stack**. |
| Act / Scene headings | Labels, numbered in Roman numerals. Execution falls through them top to bottom. |
| `[Enter …]` / `[Exit …]` / `[Exeunt]` | Scope management. Exactly **two** characters may be on stage when anyone speaks, because `you` has to be unambiguous. |
| A character speaking | Statements. The speaker is `I`/`me`; the other character on stage is `you`/`thou`/`thyself`. |
| Flattery and insults | Numeric literals — see below. |

### Numbers are made of adjectives

A noun is worth `±1` depending on whether it's a nice noun or a nasty one, and
**every adjective doubles it**:

```
a rose                                        =   1   (positive noun, 0 adjectives)
a fine hero                                   =   2   (1 adjective)
a brave fine hero                             =   4   (2 adjectives)
a brave bold fine hero                        =   8   (3 adjectives)
a fine fair sweet golden mighty rose          =  32   (5 adjectives)
a fine fair sweet golden mighty noble rose    =  64   (6 adjectives)
a stinking fat-kidneyed codpiece              =  -4   (negative noun)
nothing                                       =   0
```

So constants are built as `± 2^(number of adjectives)`. Anything that isn't a
power of two has to be assembled with arithmetic, which is why printing a
three-character prompt takes eight sentences.

### The statements used in this program

| Sentence | Meaning |
|---|---|
| `You are as fine as a rose.` | `you = 1` (assignment; the adjective after `as` is decoration) |
| `You are as good as the sum of yourself and me.` | `you = you + me` |
| `You are as big as the difference between me and yourself.` | `you = me - you` |
| `Listen to your heart.` | read an integer from stdin into `you` |
| `Open your heart!` | print `you` as a **number** |
| `Speak your mind!` | print `you` as a **character** (ASCII) |
| `Are you worse than a rose?` | set the global condition flag to `you < 1` |
| `Are you as good as nothing?` | set the global condition flag to `you == 0` |
| `If so, let us proceed to Scene IV.` | jump if the flag is true |
| `If not, let us return to Scene III.` | jump if the flag is false |

There is **exactly one** condition flag for the whole program, and it's global.
Of course it is.

## Running it

The interpreter is [`shakespearelang`](https://pypi.org/project/shakespearelang/)
1.0.0 — pure Python, no compiled extensions, so **all three platforms work
identically**. Needs Python 3.8+ (tested on 3.14).

### macOS / Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install shakespearelang
shakespeare run Fibonacci.spl
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install shakespearelang
shakespeare run Fibonacci.spl
```

### Windows (cmd.exe)

```bat
py -m venv .venv
.venv\Scripts\activate.bat
pip install shakespearelang
shakespeare run Fibonacci.spl
```

**Why the virtualenv?** On macOS (Homebrew Python) and most current Linux
distros, a bare `pip install` fails with `error: externally-managed-environment`
(PEP 668). A venv sidesteps it everywhere. If you'd rather have it on `PATH`
permanently, `pipx install shakespearelang` works on all three platforms.

**Tested:** macOS (arm64, Python 3.14.7). Linux and Windows follow from the same
pip install with no platform-specific steps — pure-Python package, pure-Python
dependencies (`click`, `tatsu`) — but they have not been run here.

### The debugger

Worth it. It steps through the play and prints the value of every character plus
who is currently on stage, which is the only sane way to understand an SPL
program you didn't just write:

```sh
shakespeare debug Fibonacci.spl
```

`shakespeare console` also gives you a REPL with Romeo and Juliet pre-declared,
for trying a sentence without writing a whole play.

## `Fibonacci.spl`

Asks for `n`, prints the n'th Fibonacci number.

```
$ shakespeare run Fibonacci.spl
N? 10
55
```

Indexing is `fib(0) = 0`, `fib(1) = 1`, `fib(2) = 1`, `fib(10) = 55`.

### The cast, and what they actually are

| Character | Role |
|---|---|
| **Romeo** | `a` — the current Fibonacci number. The answer, eventually. |
| **Juliet** | `b` — the next one. Always one ahead of Romeo. |
| **Ophelia** | `n` — the loop counter, counted down to zero. Also doubles as scratch space while the prompt is printed. |
| **The Ghost** | Pure verb. Holds no value; exists so that somebody can address Ophelia, since `you` needs a speaker. |

### The plot, as an algorithm

```
Scene I     Romeo, Juliet = 0, 1
Scene II    print "N? "; read n into Ophelia
            if n < 1: goto Scene IV          <- guards n = 0, and avoids a do-while
Scene III   Romeo, Juliet = Juliet, Romeo + Juliet
            n = n - 1
            if n != 0: goto Scene III
Scene IV    print Romeo, then a newline
```

### The trick worth stealing

A Fibonacci step is a simultaneous update, `(a, b) ← (b, a+b)`, and SPL has no
temporary variables — only the two characters currently on stage. The play does
it in two sentences with no temp at all:

```
Romeo:
 You are as good as the sum of yourself and me.      -- Juliet = b + a
Juliet:
 You are as big as the difference between me and yourself.   -- Romeo = (a+b) - a = b
```

Romeo's old value is used to *recover* his new one from Juliet, so the swap
destroys nothing. (The alternative is `Juliet: Remember me.` … `Juliet: Recall
your happy childhood!`, pushing `b` onto Romeo's stack and popping it back —
also fine, but it needs three sentences and a stack.)

### The other trick: staging is control flow

Only two characters can be on stage, but the loop needs three variables. So the
stage is re-cast mid-scene — the lovers do the arithmetic, exit, and the Ghost
and Ophelia come on to do the counting.

That means every jump target has an **entry invariant**: whichever path you
arrive by, the same two characters must be standing there. Both entrances to
Scene III (falling out of Scene II, and looping back from Scene III's own last
line) leave The Ghost and Ophelia on stage, and both entrances to Scene IV do
too. Each scene then opens with `[Exeunt]` to clear the boards. Get this wrong
and the interpreter fairly points out that `you` is ambiguous with four people
in the room.

### Why the prompt is eight sentences

`N? ` is character codes 78, 63, 32. Only 32 and 64 are powers of two, so:

```
78 = 64 + 8 + 4 + 2     ('N')  -> four sentences
63 = 64 - 1             ('?')  -> two sentences
32 = 2^5                (' ')  -> one sentence, at last
```

Plus a `Speak your mind!` after each. The closing newline (10 = 8 + 2) gets
folded into one sentence as `the sum of a brave bold fine hero and a fine hero`.

## Known wart

`shakespearelang`'s number reader rejects a leading minus sign, so you cannot
type a negative `n` — it errors with *"No numeric input was given."* The play's
own `Are you worse than a rose?` guard would handle negatives correctly (it
would print `0`); the input layer just never lets one through.
