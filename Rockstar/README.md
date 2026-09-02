# Rockstar

A language designed so that developers could **legitimately** put "rockstar
developer" on their CV. Created by Dylan Beattie in 2018 after one too many
job ads asking for one.

Programs are power ballads. Valid Rockstar is meant to be singable, and the
canonical example programs read like someone workshopping lyrics at 2am.

Unusually for this repo, Rockstar is *good*. The v2 interpreter has functions,
closures, arrays, string manipulation, proper number handling, and a REPL. The
joke is the syntax, not the semantics.

## The core conceit

Every construct is a lyric. Assignment is `Put … into …`, arithmetic is `with`
and `without`, and increment is `Build my world up`.

| Normal language | Rockstar |
|---|---|
| `x = 5` | `Put 5 into my heart` / `My heart is 5` |
| `x = x + y` | `Put my heart with your love into my heart` |
| `x++` / `x--` | `Build my heart up` / `Knock my heart down` |
| `print x` | `Shout x` — also `Say`, `Scream`, `Whisper`, `Write` |
| `input()` | `Listen to my heart` |
| `int(s)` | `Cast my heart with 10` |
| `while (…) {}` | `While …` … `end` |
| `if (…) {}` | `If …` … `end` |
| `break` / `continue` | `Break it down` / `Take it to the top` |
| `// comment` | `(comment)` |

Arithmetic has lyrical aliases: `with`/`plus`, `without`/`minus`, `times`/`of`,
`over`/`between`. Comparison is `is higher than`, `is lower than`,
`is as high as`.

### Variable names are two flavours

- **Common variables** — `a`, `an`, `the`, `my`, `your`, `our` plus a lowercase
  word: `my sorrow`, `the night`, `your heart`.
- **Proper variables** — capitalised words: `Tommy`, `Gina`, `Mister Crowley`.

Which is why Rockstar code accidentally reads like it means something.

### Poetic number literals — the signature feature

Assign with `is` followed by *words* instead of digits, and each word becomes a
digit equal to **its letter count mod 10**:

```rockstar
My sorrow is melancholy          (one 10-letter word         -> 0)
My hope is a                     (one 1-letter word          -> 1)
My hope is a lonely rockstar     (1, 6, 8                    -> 168)
Tommy is a rebel without a cause (1, 5, 7, 1, 5              -> 15715)
```

This is why the program below opens with `My sorrow is melancholy` rather than
`Put 0 into my sorrow`. It means exactly the same thing and sounds considerably
worse about it.

### Two syntax traps

- **Comments are parentheses**, so Rockstar has **no parentheses in
  expressions** at all. Precedence is the usual mathematical convention and you
  cannot override it — restructure into multiple statements instead.
- **A blank line ends a block.** There is no indentation-based scoping. Blocks
  close on an empty line, or on `end` (aliases: `oh`, `yeah`, `baby`, and `oooh`
  which closes one block per `o`). So a stray blank line inside a loop silently
  ends the loop early.

## Running it

Upstream ships **official prebuilt binaries for all three platforms** on the
[releases page](https://github.com/RockstarLang/rockstar/releases) — no compiler,
no runtime, no package manager. Version used here: **v2.0.31**.

Each archive extracts to a folder containing a single self-contained executable.

There are two songs in this folder, `HelloWorld.rock` and `Fibonacci.rock`.
Both run as `rockstar <file>`.

### macOS

```sh
# Apple Silicon; use -macos-x64 for Intel
curl -LO https://github.com/RockstarLang/rockstar/releases/download/v2.0.31/rockstar-v2.0.31-macos-arm64.tar.gz
tar xzf rockstar-v2.0.31-macos-arm64.tar.gz
./rockstar-macos-arm64-binary/rockstar Fibonacci.rock
```

If you download it with a **browser** rather than `curl`, Gatekeeper will
quarantine it and refuse to run it. Clear that with:

```sh
xattr -d com.apple.quarantine ./rockstar-macos-arm64-binary/rockstar
```

### Linux

```sh
curl -LO https://github.com/RockstarLang/rockstar/releases/download/v2.0.31/rockstar-v2.0.31-linux-x64.tar.gz
tar xzf rockstar-v2.0.31-linux-x64.tar.gz
./rockstar-linux-x64-binary/rockstar Fibonacci.rock
```

### Windows (PowerShell)

```powershell
curl.exe -LO https://github.com/RockstarLang/rockstar/releases/download/v2.0.31/rockstar-v2.0.31-windows-x64.zip
Expand-Archive rockstar-v2.0.31-windows-x64.zip -DestinationPath .
.\rockstar-windows-x64-binary\rockstar.exe Fibonacci.rock
```

### No install at all

There's an official browser playground at
**<https://codewithrockstar.com/online>** — paste the program in and hit
Cmd/Ctrl-Enter. Genuinely the fastest route if you just want to see it run.

### From source

Needs the **.NET 9 SDK**:

```sh
git clone https://github.com/RockstarLang/rockstar.git
cd rockstar
dotnet build ./Starship/Starship.sln
```

`rockstar` with no arguments starts a REPL. `rockstar <file>` and
`rockstar run <file>` are equivalent.

### What was actually tested

| Platform | Status |
|---|---|
| macOS (arm64, v2.0.31 prebuilt binary) | tested — every output below verified |
| Linux (x64 prebuilt) | archive contents verified; binary not run here |
| Windows (x64 prebuilt) | archive contents verified; binary not run here |

## `HelloWorld.rock`

Shouts `Hello, World!` without containing a single letter of it.

```
$ rockstar HelloWorld.rock
Hello, World!
```

`Shout "Hello, World!"` would have been one line. Instead the greeting is
written entirely in **poetic number literals** — the one feature that makes
Rockstar Rockstar — so the song's lyrics *are* the character codes:

```rockstar
My heart is burning up                             (7 2     -> 72  -> H)
My echo is a loneliness everlasting                (1 10 11 -> 101 -> e)
My longing is a melancholy farewell                (1 10 8  -> 108 -> l)
My ocean is heartbroken, unbreakable, everlasting  (11 11 11 -> 111 -> o)
```

Rockstar counts the letters in each word and takes that count **modulo ten** as
one decimal digit. So `burning up` is 7 then 2, which is 72, which is a capital
`H`. `everlasting` is eleven letters and therefore a `1`, which is what makes
`o` sayable at all: 111 needs three odd-length words in a row, and three
one-letter words in a row is not a lyric.

### Cast turns a number into a letter

```rockstar
Cast my heart
Let the song be my heart with my echo with my longing with my longing
Shout the song
```

`Cast` is Rockstar's type conversion, and which conversion you get depends on
what you hand it:

| | Result |
|---|---|
| `Cast 72 into X` | number → the character it codes for, so `X` is `"H"` |
| `Cast my heart` | the same conversion, in place |
| `Cast "123" with 10` | string → number in the given base, so `123` |
| `Cast "123"` | string → **array** of code points, `[ 49, 50, 51 ]` |

`Fibonacci.rock` uses the third form (`Cast your heart with 10`) to turn typed
input into a number; this program uses the second. The fourth is a trap and is
filed under warts below.

Because `with` is addition — which on strings means concatenation — the greeting
then assembles in three `Let … be` lines.

### Ten literals, thirteen letters

`Hello, World!` has thirteen characters and only ten distinct ones. Each gets one
variable, and repeats simply name it again: `my longing` is shouted three times
as the three `l`s, `my ocean` twice as the two `o`s. The closing newline is not
in the song at all — `Shout` supplies it, exactly as `Write` withholds it for the
`N? ` prompt in the other program.

`my finale` is the nicest of the ten. `!` is 33, which needs two three-letter
words, and the two three-letter words are **`the end`**.

### The wart that is not a wart

`end` closes a block in Rockstar, and `My finale is the end` looks alarmingly
like an unbalanced one. It parses correctly: once `is` starts a poetic literal
the rest of the line is counted rather than executed, so the keyword never
reaches the parser as a keyword. Verified — it yields 33, not a syntax error.

The same rule covers the parenthetical comments above. Rockstar strips them
before counting the lyric, which is the only reason those annotations can sit on
the same line as the literals they annotate.

The real trap is **`Cast` on a string with no radix**. It does not parse the
string — it explodes it into an array of code points, and an array in numeric
context is its own length, so `Cast "123" into X` followed by `X with 1` prints
`4` rather than `124`. Always give `Cast` a base when the input is text; that is
what `with 10` is doing in `Fibonacci.rock`.

## `Fibonacci.rock`

Asks for `n`, shouts the n'th Fibonacci number. Output is byte-identical to the
[Shakespeare](../Shakespeare/) and [LOLCODE](../LOLCODE/) versions.

```
$ rockstar Fibonacci.rock
N? 10
55
```

### How it works

```rockstar
While the night is higher than 0
Put my sorrow with my hope into the future
Put my hope into my sorrow
Put the future into my hope
Knock the night down
end
```

`my sorrow` is the answer, `my hope` is always one Fibonacci number ahead,
`the future` is the temporary, and `the night` counts down. `Write "N? "` is the
one output verb that omits the trailing newline, which is how the prompt matches
the other two languages exactly.

**Rockstar needs no guard for `n <= 0`.** `While the night is higher than 0`
tests before the first pass, so `n = 0` runs zero iterations and shouts the
initial `0`, and a negative `n` does the same. Shakespeare needed an explicit
scene jump to dodge a do-while; LOLCODE needed an explicit `n < 0` check because
`GIMMEH` happily accepts negatives. Rockstar gets both for free.

### The same problem, three ways

| | Shakespeare | LOLCODE | Rockstar |
|---|---|---|---|
| Temp variable | none — swap done arithmetically | `nxt` | `the future` |
| `n <= 0` | explicit scene-jump guard | explicit `n < 0` guard | free |
| Numeric type | Python ints, unbounded | signed 64-bit, wraps at `n=93` | .NET `decimal`, exact to `n=138` |
| Reads like | a stage play | a cat | a power ballad |

## Known warts

Both are `lci`-style rough edges in the interpreter, documented rather than
worked around:

- **Non-numeric input dumps a raw .NET stack trace.** Typing `rockstar` at the
  prompt produces an unhandled `System.FormatException` with a full managed
  backtrace. `Cast` has no soft-failure mode.
- **Numbers are .NET `decimal`, and overflow is fatal rather than silent.** Exact
  through **`n = 138`** (`30960598847965113057878492344` — 29 digits, far past
  what LOLCODE's 64-bit `NUMBR` manages). At `n = 139` it dies with
  `System.OverflowException`. Note it fails one step *earlier* than you'd expect:
  `decimal` could hold `fib(139)`, but the loop always computes one number ahead,
  and `fib(140)` exceeds the maximum.

On the plus side, being exact to 29 digits makes Rockstar the best-behaved
numeric implementation of the three — it gets `fib(93)` right, which is precisely
where LOLCODE silently wraps into a negative number.
