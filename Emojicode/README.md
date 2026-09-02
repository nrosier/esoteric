# Emojicode

Emojicode is the odd one out in this repo. The other five languages are jokes
that happen to run; Emojicode is a **real language** that happens to be spelled
in emoji. It has classes, value types, protocols, generics, closures, optionals,
a type checker that will tell you off, and an LLVM backend that emits a native
executable. Upstream's own one-line summary is not kidding:

> Emojicode is an open source, high-level, multi-paradigm programming language
> consisting of emojis. It features Object-Orientation, Optionals, Generics and
> Closures.

Started on New Year's Eve 2015 by Theo B. Weidmann, 34 releases since, and
around 3,400 stars. The latest release is **1.0 beta 2** from February 2020;
the last commit to `master` is from August 2023. Beta since 2019, in other
words, which is the most honest thing about it.

The consequence of being a real language: this is the only folder in the repo
whose programs are **compiled**, and the only one where the interpreter has
opinions about your code style.

## The core conceit

Every type, method and initializer name is an emoji. Your own variable names
are plain text — and *must* be, because emoji are the language's vocabulary,
not yours.

| Normal language | Emojicode |
|---|---|
| `// comment` | `💭 comment` |
| `main()` | `🏁 🍇` … `🍉` |
| `{` … `}` | `🍇` … `🍉` |
| `x = 5` | `5 ➡️ 🖍🆕 x` — the value comes **first** |
| `x = 6` (reassign) | `6 ➡️ 🖍 x` |
| `x += 1` | `x ⬅️➕ 1` |
| `print(s)` | `😀 s❗️` |
| `print(s, end="")` | `👄 s❗️` |
| `if a > b … else …` | `↪️ a ▶️ b 🍇🍉 🙅 🍇🍉` |
| `else if` | `🙅↪️` |
| `while c` | `🔁 c 🍇🍉` |
| `for i in range(0, 10)` | `🔂 i 🆕⏩ 0 10❗️ 🍇🍉` |
| `(a + b) * c` | `🤜a ➕ b🤛 ✖️ c` |
| `a % b` | `a 🚮 b` |
| `class Foo` | `🐇 🦊 🍇🍉` |
| `struct Foo` | `🕊 🦊 🍇🍉` |
| `interface` / `protocol` | `🐊 🗣 🍇🍉` |
| `Foo()` | `🆕🦊❗️` |
| `self` | `👇` |
| `return x` | `↩️ x` |
| `Optional<Int>` | `🍬🔢` |
| `null` | `🤷‍♀️` |
| `x!` (force unwrap, may panic) | `🍺 x` |
| `if let y = x` | `↪️ x ➡️ y 🍇🍉` |
| `f"…{x}…"` | `🔤…🧲x🧲…🔤` |
| `[1, 2, 3]` | `🍿 1 2 3 🍆` |
| `List<String>` (the type) | `🍨🐚🔡🍆` |
| `list.append(v)` | `🐻 list v❗️` |
| `str(n)` | `🔡 n❗️` |
| `int(s, 10)` | `🔢 s 10❗️` → an **optional** |
| `s.strip()` | `🔧 s❗️` |
| `input()` | `🆕🔡▶️👂🏼❗️` |
| `exit(1)` | `🚪 🐇💻 1❗️` |

### Assignment points at the destination

```
31 ➡️ daysInDecember
```

The value is on the left and the variable on the right, because the arrow points
at where the value is going. Every other language in this repo puts the
destination first; this one is arguably the sensible one and it still feels
wrong for about an hour.

### Calls are prefix, and end in a mood

A call is *method, receiver, arguments, terminator*:

```
😀 🔤hi🔤❗️            💭 call 😀 on the string "hi"
🔡 n❗️                💭 call 🔡 on n, giving a string
🔪 🔤Apples🔤 2 4❗️     💭 call 🔪 on "Apples" with 2 and 4, giving "ples"
```

The terminator is the method's **mood** and it is part of the name: `❗️` is
imperative, `❓` is interrogative. `🐻` (append) is an `❗️` method and `📏`
(length) is a `❓` method, so you write `🐻 words x❗️` but `📏 words❓`. Getting
the mood wrong is a compile error, which is a sentence that should not make
sense.

### The type system is not part of the joke

```
🐊 🗣 🍇          💭 a protocol
  ❗️ 💬 ➡️ 🔡      💭 …with one method returning a string
🍉
```

Protocols, generics (`🍨🐚🔡🍆` is `List<String>`), inheritance, access levels
(`🔓` public, `🔒` package, `🔐` protected), and optionals that you cannot use
without acknowledging they might be empty. The compiler also lints: declare
something with `🖍` and never mutate it and you get

```
⚠️  warning: Variable "nxt" was never mutated; consider making it a constant variable.
```

which is more than several non-esoteric languages manage.

## Running it

This is the part that takes the afternoon. Upstream ships prebuilt tarballs for
**Darwin x86_64** and **Linux x86_64**, and that is the entire list: no arm64
build, no Windows build, no package in Homebrew or apt.

### macOS, Apple Silicon — tested, via Rosetta 2

The shipped compiler is an x86_64 Mach-O, so on an M-series Mac it runs under
Rosetta 2, and — this is the part worth knowing — **the executables it produces
are also x86_64**, so they need Rosetta too.

```bash
softwareupdate --install-rosetta        # once, if you have never needed it

curl -LO https://github.com/emojicode/emojicode/releases/download/v1.0-beta.2/Emojicode-1.0-beta.2-Darwin-x86_64.tar.gz
tar xzf Emojicode-1.0-beta.2-Darwin-x86_64.tar.gz
cd Emojicode-1.0-beta.2-Darwin-x86_64
./install.sh                            # asks for confirmation, then offers sudo
```

`install.sh` copies `emojicodec` to `/usr/local/bin`, the packages to
`/usr/local/EmojicodePackages` and the headers to `/usr/local/include/emojicode`.
On Apple Silicon `/usr/local` is not Homebrew's prefix and usually is not
writable, so it will offer to re-run itself with `sudo`. Then:

```bash
emojicodec Emojicode/HelloWorld.emojic
Emojicode/HelloWorld
```

### Without installing anything system-wide — what was actually done here

You do not have to let a beta compiler write into `/usr/local`. `-S` adds a
package search path, which is all `install.sh` was really arranging:

```bash
EC=~/Emojicode-1.0-beta.2-Darwin-x86_64          # wherever you extracted it

$EC/emojicodec -S"$EC/packages" Emojicode/HelloWorld.emojic
Emojicode/HelloWorld
```

Both programs in this folder were compiled and verified exactly this way. Without
the `-S` you get:

```
🚨 error: Could not find package s.
ℹ️ note: Searched in:
/your/current/directory/packages
/usr/local/EmojicodePackages
```

The compiler needs a working `c++` on `PATH` either way, because it shells out to
link. The resulting binary is self-contained apart from the system libraries —
`otool -L` shows only `libSystem` and `libc++`, no Emojicode runtime to ship.

### macOS, Intel

The same `Darwin-x86_64` tarball, natively, no Rosetta. Not run here — this
machine is arm64 — but it is the same binary that Rosetta is emulating.

### Linux

```bash
curl -LO https://github.com/emojicode/emojicode/releases/download/v1.0-beta.2/Emojicode-1.0-beta.2-Linux-x86_64.tar.gz
tar xzf Emojicode-1.0-beta.2-Linux-x86_64.tar.gz
cd Emojicode-1.0-beta.2-Linux-x86_64
./install.sh
```

You need `clang++` or `g++` installed for the link step. x86_64 only — an
aarch64 Linux box is in the same position as an Apple Silicon Mac, minus
Rosetta. Not run here.

### Windows

There is no Windows build, and upstream does not pretend otherwise: its install
page tells Windows users to use Bash on Ubuntu on Windows and follow the Linux
instructions. So:

```powershell
wsl --install                  # then, inside the WSL shell, the Linux steps above
```

Not run here. This is the WSL case house rule 6 exists for.

### From source — the only route to a native arm64 binary

Prerequisites, per upstream's README: clang 6.0.1 or gcc 7.2, CMake 3.5.1+
(Ninja preferred), **LLVM 7**, and Python 3.5.2+ for the test suite.

```bash
git clone https://github.com/emojicode/emojicode
cd emojicode && mkdir build && cd build
cmake .. -GNinja && ninja
```

Not attempted. LLVM 7 is from 2018 and Homebrew currently ships LLVM 21; the
version gap is the whole reason there is no arm64 build to download in the first
place. If you want native arm64 Emojicode, budget an evening for LLVM API
archaeology, not five minutes.

### What was actually tested

| Platform | Status |
|---|---|
| macOS 26.6.2 (arm64) via Rosetta 2, Emojicode 1.0 beta 2 | tested — both programs compiled and every output below verified |
| macOS (x86_64) | not run here; identical binary, minus the emulation |
| Linux (x86_64) | not run here; upstream tarball and `install.sh` |
| Linux (aarch64) | no build exists; source build only |
| Windows | no build exists; upstream points at WSL |

There is no `--version` flag (`emojicodec --version` answers
`👉 Flag could not be matched: version`). `--help` identifies itself as
"Emojicode Compiler 1.0 beta 2", which is how the version above was established.

## `HelloWorld.emojic`

```
$ emojicodec Emojicode/HelloWorld.emojic && Emojicode/HelloWorld
Hello, World!
```

The other five Hello Worlds in this repo are exercises in *getting a letter out
at all*. Emojicode can print a string literal in one line, so a one-line program
would say nothing about the language. Instead this one is deliberately
over-engineered — a protocol, a value type, a class, an optional and a generic
list, which is roughly the shape of an enterprise Java Hello World:

| Piece | What it is | Why it's there |
|---|---|---|
| `🐊 🗣` | a protocol with one method, `💬` | so the two implementations below can share a type |
| `🕊 📝` | a **value type** holding a `🔡` | words are copied when passed, like integers |
| `🐇 ✂️` | a **class** holding a `🍬🔡` | punctuation, heap-allocated and passed by reference |
| `🍿 … 🍆` | a list literal of five `🗣` | the cast, in order |
| `🍨🐚🔡🍆` | `List<String>` | what each speaker's `💬` gets appended to |
| `🆕🔡 words 🔤🔤❗️` | the join initializer | one string, no separator |
| `😀 … ❗️` | print | called exactly once, at the very end |

### The cast

```
🍿
  🆕📝 🔤Hello🔤❗️        💭 a word
  🆕✂️ 🔤, 🔤❗️           💭 punctuation that exists
  🆕📝 🔤World🔤❗️        💭 a word
  🆕✂️ 🔤!🔤❗️            💭 punctuation that exists
  🆕✂️ 🤷‍♀️❗️              💭 punctuation that does not
🍆 ➡️ cast
```

The fifth speaker is the point of the exercise. It is a `✂️` constructed with
`🤷‍♀️` — no value — and its `💬` method reaches for the optional using the
conditional-unwrap form:

```
❗️ 💬 ➡️ 🔡 🍇
  ↪️ mark ➡️ actual 🍇
    ↩️ actual
  🍉
  ↩️ 🔤🔤
🍉
```

The block runs only if there is a value, and `actual` is that value, non-optional,
inside it. There is no way to spell this that skips the check: `mark` is a `🍬🔡`
and the return type is `🔡`, so the compiler simply will not let you return it.
The empty speaker contributes an empty string, and `Hello, World!` comes out with
nothing missing and nothing crashed — which is not the behaviour any other
program in this repo would manage with a missing value.

### The inversion, out loud

Every type here — `🗣`, `📝`, `✂️` — is an emoji, and every variable —
`cast`, `words`, `speaker`, `mark`, `actual` — is plain ASCII, because the
language requires exactly that. It is the mirror image of the rest of the repo,
where the language is ASCII and the entertainment lives in the identifiers:
`Romeo`, `flour`, `my heart`, `mascarpone`.

### Verified output

```
$ Emojicode/HelloWorld | xxd
00000000: 4865 6c6c 6f2c 2057 6f72 6c64 210a       Hello, World!.
```

Fourteen bytes, byte-identical to the other five Hello Worlds here.

## `Fibonacci.emojic`

```
$ echo 10 | Emojicode/Fibonacci
N? 55
```

Same problem as the other five folders, and the only one of the six that can
decline bad input politely.

### Reading a number that might not be a number

```
👄 🔤N? 🔤❗️
🆕🔡▶️👂🏼❗️ ➡️ typed

↪️ 🔢 🔧 typed❗️ 10❗️ ➡️ n 🍇
  💭 …compute and print fib(n)…
🍉
🙅 🍇
  😀 🔤🤷 that was not a number.🔤❗️
  🚪 🐇💻 1❗️
🍉
```

Four things worth pointing at:

- **`👄` versus `😀`.** `👄` puts a string on stdout; `😀` does the same and adds
  a newline. So the prompt is `👄` and the answer is `😀`.
- **The prompt arrives before the input.** `▶️👂🏼` is an initializer on `🔡`
  that blocks until Enter. Checked on a real pty: with nothing typed yet the
  terminal already shows `N? `. Chef physically cannot do this and Emojicode does
  it without being asked.
- **`🔢 s 10❗️` returns `🍬🔢`,** an optional, because a string might not be a
  number in base 10. The `↪️ … ➡️ n` form unwraps it and binds `n` only when
  there was something to bind, so non-numeric input takes the `🙅` branch and
  exits 1. `🍺` would force it and panic instead — see the warts.
- **Negative `N` needs no guard.** The loop is `🔁 countdown ▶️ 0`, so `-3`
  never enters it and `a` stays `0`.

### The loop

```
0 ➡️ 🖍🆕 a
1 ➡️ 🖍🆕 b
n ➡️ 🖍🆕 countdown
🔁 countdown ▶️ 0 🍇
  a ➕ b ➡️ sum
  b ➡️ 🖍 a
  sum ➡️ 🖍 b
  countdown ⬅️➖ 1
🍉
😀 🔤🧲a🧲🔤❗️
```

`sum` is a constant — declared without `🖍`, fresh each iteration — so this is
the ordinary three-variable shuffle, like LOLCODE's and Rockstar's. And
`🧲a🧲` interpolates the `🔢` straight into the string literal, converting on the
way in, so no explicit `🔡 a❗️` is needed.

Note what is *not* here: a range. `🔂 i 🆕⏩ 0 n❗️` is the idiomatic way to count,
and it is a trap for exactly this program — see the warts.

### Verified output

```
$ echo 10  | Emojicode/Fibonacci
N? 55
$ echo 0   | Emojicode/Fibonacci
N? 0
$ echo 1   | Emojicode/Fibonacci
N? 1
$ echo -3  | Emojicode/Fibonacci
N? 0
$ echo 92  | Emojicode/Fibonacci
N? 7540113804746346429
$ echo abc | Emojicode/Fibonacci
N? 🤷 that was not a number.
$ echo $?
1
```

Checked against Python for `n = 0…92`: exact. `n = 93` and beyond: see below.

### The same problem, six ways

| | Numeric type | Exact up to | Negative `N` | Non-numeric input |
|---|---|---|---|---|
| Shakespeare | Python ints, unbounded | any | explicit guard | interpreter errors out |
| LOLCODE | signed 64-bit | `fib(92)` | explicit guard | silently becomes `0` |
| Rockstar | .NET `decimal` | `fib(138)` | free | raw .NET stack trace |
| Chef | Python ints, unbounded | any | **hangs forever** | Python traceback |
| Ook! | decimal digit arrays | any (tested to 255) | reads `-3` as `229` | reads it as digits |
| Emojicode | signed 64-bit | `fib(92)` | free | `🤷 that was not a number.`, exit 1 |

Six languages, and the one with a type checker is the only one that says
something useful when you type `abc`.

## Known warts

- **`⏩` counts backwards without being asked.** The two-argument range
  initializer infers its own direction, so `🆕⏩ 0 🔋5❗️❗️` — zero to minus five
  — has `📏` of **5** and visits `0 -1 -2 -3 -4`. Idiomatic Fibonacci
  (`🔂 i 🆕⏩ 0 n❗️`) therefore runs `|n|` times for negative `n` and cheerfully
  prints `fib(3)` for an input of `-3`. Verified; it is why this program counts
  down with an explicit `▶️ 0` instead.
- **`--format` edits your file in place and eats your comments.** There is no
  `--dry-run`, no backup, and nothing on stdout. Run on this folder's
  `HelloWorld.emojic` it took the comments from 15 lines to 4, deleted the
  header block entirely, left the survivors at column 0, collapsed the list
  literal onto one line, and added `🥯` and `🎍🥡` annotations that were not
  written. The formatted file still compiled and still printed the right
  fourteen bytes — it is a formatter, not a wrecking ball — but the explanation
  of *why* the program is shaped that way was gone. Found out the interesting
  way; the file here was restored by hand.
- **`✂️` and `✂` are two different types.** `✂️` is U+2702 U+FE0F, `✂` is bare
  U+2702, and the compiler treats them as unrelated names:
  `🚨 error: _✂ has no suitable 🆕`. Since `--format` normalises away the
  variation selector, a formatted file and an unformatted one can disagree about
  what a type is called. Your editor renders both identically. Good luck.
- **`fib(93)` wraps silently.** `🔢` is a signed 64-bit integer with no overflow
  check: `n = 93` prints `-6246583658587674878`, which is the true value minus
  2⁶⁴. Same failure mode as LOLCODE, ten digits earlier than Rockstar, and
  unlike Chef and Shakespeare, which are backed by Python ints.
- **`🍺` panics in emoji.** Force-unwrapping an empty optional aborts with
  `🤯 Program panicked: Unwrapped an optional that contained no value.
  (Fibonacci.emojic:5:6)` and exit code 134. The source location is genuinely
  useful; SIGABRT for bad user input is not, which is why this program does not
  use `🍺`.
- **No `--version`.** `emojicodec --version` replies
  `👉 Flag could not be matched: version`. You get the version out of `--help`.
- **`install.sh` wants `/usr/local` and offers to `sudo` itself.** It is an
  interactive script that re-executes itself as root if the target is not
  writable. `-S` avoids the whole question.
- **Beta since 2019, x86_64 only.** 1.0 beta 2 is from February 2020, the last
  commit is from August 2023, and no arm64 binary has ever been published — for
  either macOS or Linux. The language is finished enough to be pleasant and
  unfinished enough that you should not expect a fix.

## Is it actually usable?

Uncomfortably close to yes. Once the tarball is unpacked, the loop is
edit-compile-run with sub-second compiles, the diagnostics are better than some
mainstream compilers (`🚨 error: s🔡 has no suitable ➕`, complete with a `⬆️`
pointing at the column, plus `ℹ️ note:` lines citing the standard library's own
source), and the output is an ordinary native executable with no runtime to
install.

The catch is not the emoji. It is that typing the emoji is genuinely slow — every
line here was assembled by copy-paste and picker — and that the identifiers you
are allowed to name yourself are the boring half. Emojicode is the only language
in this repo where the joke is that it *works*.
