# LOLCODE

A programming language built entirely out of 2007 lolcat captions. Created by
Adam Lindsay in that same year, when the internet was mostly cats with bad
grammar. It is far more complete than the joke requires: variables, type
coercion, loops, conditionals, functions, exceptions.

Programs open with `HAI` and close with `KTHXBYE`, and are legible to anyone who
was online in 2007 and nobody else.

## The core conceit

Take an ordinary imperative language and rename every single keyword to
something a cat would say.

| Normal language | LOLCODE |
|---|---|
| `main() {` … `}` | `HAI 1.2` … `KTHXBYE` |
| `int x = 0;` | `I HAS A x ITZ 0` |
| `x = 5;` | `x R 5` |
| `print(x)` | `VISIBLE x` |
| `scanf(x)` | `GIMMEH x` |
| `x = (int) x` | `x IS NOW A NUMBR` |
| `if (c) {…} else {…}` | `c` / `O RLY?` / `YA RLY` … `NO WAI` … `OIC` |
| `while` / `for` | `IM IN YR loop` … `IM OUTTA YR loop` |
| `break` | `GTFO` |
| `// comment` | `BTW comment` |
| `/* comment */` | `OBTW` … `TLDR` |

### Arithmetic is prefix, and spelled out loud

There are no operators. Every calculation is a phrase, with `AN` separating the
arguments:

```
SUM OF a AN b            a + b
DIFF OF a AN b           a - b
PRODUKT OF a AN b        a * b
QUOSHUNT OF a AN b       a / b
MOD OF a AN b            a % b
BIGGR OF a AN b          max(a, b)
SMALLR OF a AN b         min(a, b)
BOTH SAEM a AN b         a == b
DIFFRINT a AN b          a != b
```

Because it's prefix, nesting works without parentheses —
`BIGGR OF n AN 0` drops straight into another expression. Note there is **no
less-than operator**; you build comparisons out of `BOTH SAEM` and
`BIGGR OF`/`SMALLR OF`. This program needs `n < 0`, which becomes:

```
DIFFRINT n AN BIGGR OF n AN 0        BTW  n != max(n, 0), i.e. n < 0
```

### `IT`, the implicit variable

`O RLY?` takes no condition. It tests `IT`, a magic global holding the value of
the last bare expression evaluated. So a conditional is *two statements*: one
that computes a truth value, then `O RLY?` which reads it. Every bare expression
you write clobbers `IT`.

## Running it

```sh
brew install lolcode
lci Fibonacci.lol
```

Verified with `lci` 1.3 (the reference C implementation, by Justin Meza).

**Gotcha worth knowing:** the binary is called `lci`, and Homebrew *also* has a
formula literally named `lci` — which is an unrelated **lambda calculus**
interpreter that installs a binary with the same name. The two formulae conflict.
You want `brew install lolcode`. Installing `lci` gets you a very confused
lambda evaluator emitting `syntax error after '.'` at your cat.

## `Fibonacci.lol`

Asks for `n`, prints the n'th Fibonacci number. Same interface and same
byte-for-byte output as [../Shakespeare/Fibonacci.spl](../Shakespeare/Fibonacci.spl).

```
$ lci Fibonacci.lol
N? 10
55
```

Indexing is `fib(0) = 0`, `fib(1) = 1`, `fib(10) = 55`.

### How it works

Refreshingly: it just works. After Shakespeare, LOLCODE is a holiday — it has
named variables, real assignment, and a loop construct that takes a counter and
a termination test on one line.

```
IM IN YR ladder UPPIN YR i TIL BOTH SAEM i AN n
    nxt R SUM OF a AN b
    a R b
    b R nxt
IM OUTTA YR ladder
```

`UPPIN YR i` increments `i` each pass, `TIL <expr>` loops *until* the expression
becomes true. Two details make the edge cases free:

- **`TIL` tests before each iteration**, not after. So `n = 0` climbs zero rungs
  and `a` is still `0` — `fib(0)` falls out for nothing. The Shakespeare version
  had to bolt on an explicit guard to dodge a do-while.
- **A real temporary variable exists.** `nxt` holds `a + b` while `a` is
  overwritten. Shakespeare has no temporaries, so it had to reconstruct the swap
  arithmetically. Here it's three boring lines, and that contrast is the whole
  reason to write the same program twice.

`nxt` and `i` are declared before the loop rather than inside it, since
`I HAS A` in a loop body would re-declare on every pass.

## Known warts

Both of these are real `lci` behaviours, not bugs in the program:

- **Garbage input silently becomes zero.** `IS NOW A NUMBR` does not fail on
  unparseable input — it yields `0`. So typing `kitteh` prints `0` rather than
  complaining. Cats do not do error handling.
- **`NUMBR` is a signed 64-bit integer, and it wraps.** Correct through
  `n = 92` (`7540113804746346429`); at `n = 93` it silently rolls over to
  `-6246583658587674878`. No overflow warning, because of course not.

On the plus side, `GIMMEH` reads negative numbers perfectly well, so the `n < 0`
guard actually gets exercised — unlike in Shakespeare, where the interpreter's
number reader refuses a leading minus and the equivalent guard is unreachable.
