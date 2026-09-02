# Chef

Chef was designed by David Morgan-Mar in 2002 on one gloriously stupid premise:
**programs should look like recipes.** Not "recipe-flavoured syntax" — actual
recipes, with an ingredients list, a method in numbered-sounding prose, and a
serving suggestion at the bottom. The language's design principles say it out
loud:

> Program recipes should not only generate valid output, but be easy to prepare
> and delicious.

So a Chef program has two audiences: the interpreter, and a hungry person. This
folder's program is a fruitcake that happens to compute Fibonacci numbers.

## The core conceit

| Normal language | Chef |
|---|---|
| `x = 5` | `5 g flour` in the ingredients list |
| `input()` | `Take flour from refrigerator.` |
| `push x` | `Put flour into the mixing bowl.` |
| `x = pop()` | `Fold flour into the mixing bowl.` |
| `top += x` | `Add flour to the mixing bowl.` |
| `top -= x` | `Remove flour from the mixing bowl.` |
| `top *= x` | `Combine flour into the mixing bowl.` |
| `while (x != 0) {}` | `Chop the flour.` … `Chop the flour until chopped.` |
| `break` | `Set aside.` |
| `f()` | `Serve with sauce.` |
| `print` | `Pour contents of the mixing bowl into the baking dish.` + `Serves 1.` |
| `// comment` | the paragraph under the title |

## The data model: bowls, dishes and two kinds of ingredient

- **Ingredients are the variables.** They get their initial values in the
  ingredients list (`0 g flour`), or from stdin via the refrigerator.
- **Mixing bowls are stacks.** Arithmetic never touches two variables directly;
  it always operates on the value sitting on top of a bowl.
- **Baking dishes are the output.** You pour a bowl into a dish, and `Serves N`
  prints the first N dishes — **from the top down**, which is why anything you
  want printed first has to go in last.
- **Dry ingredients print as numbers; liquid ingredients print as Unicode
  characters.** The measure decides which: `g`, `kg`, `pinch` are dry; `ml`,
  `l`, `dash` are liquid; `cups`, `teaspoons` are either. `Liquefy` converts.

That last rule is the whole trick behind text output in Chef: `72 ml water` is
the letter `H`.

## Three things that bite

**1. There are no conditionals. At all.** No `if`, no comparison operators.
The only branch in the entire language is the loop: `Verb the ingredient` enters
the body if that ingredient is non-zero, and `Verb until verbed` decrements it
and goes back. Everything conditional has to be smuggled into "is this value
zero or not". This is why the program below can't guard against a negative N
the way the other three languages do — see [Known warts](#known-warts).

**2. Output is deferred to the very end.** Nothing reaches the terminal until
the recipe is served, so a Chef program physically cannot print a prompt and
*then* read input. Piped, you can't tell; interactively, you type your number
into an empty screen and the `N? ` shows up afterwards.

**3. Blank lines are structural.** Title, comment, `Ingredients.`, `Method.`
and `Serves` are separated by blank lines, and `chef-lang` wants a blank line
*after* `Serves 1.` too — without it you get
`ValueError: Invalid script format, please provide a valid recipe (no serves)`,
which is a confusing thing to be told about a file that plainly has a `Serves`
line in it.

## Running it

The interpreter used here is [`chef-lang`](https://pypi.org/project/chef-lang/)
0.1.0 from PyPI — pure Python, no dependencies, needs Python 3.10+. It installs
a single command, `cook`, which takes exactly one argument: the recipe file.
(There are no flags. `cook --help` tries to open a file named `--help`.)

Two recipes live here: `HelloWorld.chef` needs no input, and
`Fibonacci.chef` reads a number from stdin. The commands below use the
Fibonacci one because it is the one with a pipe in it.

### macOS

```bash
python3 -m venv ~/.venvs/chef
~/.venvs/chef/bin/pip install chef-lang
echo 10 | ~/.venvs/chef/bin/cook Chef/Fibonacci.chef
```

The venv is not optional politeness: Homebrew's Python is marked
externally-managed (PEP 668), so a bare `pip install` into it fails with
`error: externally-managed-environment`.

### Linux

Identical — it's pure Python:

```bash
python3 -m venv ~/.venvs/chef
~/.venvs/chef/bin/pip install chef-lang
echo 10 | ~/.venvs/chef/bin/cook Chef/Fibonacci.chef
```

On Debian/Ubuntu you may need `sudo apt install python3-venv` first. Distro
Pythons older than 3.10 won't do — `chef-lang` declares `requires-python
>=3.10`.

### Windows (PowerShell)

```powershell
py -m venv $env:USERPROFILE\.venvs\chef
& "$env:USERPROFILE\.venvs\chef\Scripts\pip.exe" install chef-lang
"10" | & "$env:USERPROFILE\.venvs\chef\Scripts\cook.exe" Chef\Fibonacci.chef
```

### Windows (cmd.exe)

```bat
py -m venv %USERPROFILE%\.venvs\chef
%USERPROFILE%\.venvs\chef\Scripts\pip.exe install chef-lang
echo 10 | %USERPROFILE%\.venvs\chef\Scripts\cook.exe Chef\Fibonacci.chef
```

### Interactively

```bash
~/.venvs/chef/bin/cook Chef/Fibonacci.chef
```

Type a number, press Enter. Remember wart #2: the `N? ` prompt arrives *after*
your answer, not before.

### Other interpreters

- **The reference Perl interpreter**, `Chef.pl`, ships with the language spec at
  <https://www.dangermouse.net/esoteric/chef.html>.
- **`rchef`** is a Rust implementation (`cargo install rchef`).

Neither was used here, so neither is claimed to run this file unchanged —
Chef implementations disagree cheerfully about corner cases.

### What was actually tested

| Platform | Status |
|---|---|
| macOS 26.6.2 (arm64, CPython 3.14.7, `chef-lang` 0.1.0) | tested — every output below verified |
| Linux | not run here; same pure-Python install, no platform-specific code |
| Windows | not run here; same pure-Python install, no platform-specific code |

## `HelloWorld.chef`

```
$ cook Chef/HelloWorld.chef
Hello, World!
```

```
Ingredients.
72 g butter
101 g caster sugar
108 g plain flour
111 g ground almonds
44 g cocoa powder
32 g candied peel
87 g mascarpone
114 g dark chocolate
100 g icing sugar
33 g runny honey
```

Ten ingredients, and every quantity is a character code. There is no arithmetic
in this recipe at all — no loop, no `Add`, no `Fold`. It is thirteen `Put`s, one
`Liquefy` and a `Pour`, which makes it the only program in this repo that does
no computing whatsoever.

### Dry ingredients print as numbers, liquid ones as letters

This is the whole trick. An ingredient's **measure** decides how it prints:

| Measure | Type | Prints as |
|---|---|---|
| `g`, `kg`, `pinch`, `pinches` | dry | the number, `72` |
| `ml`, `l`, `dash`, `dashes` | liquid | the character, `H` |
| `cup`, `teaspoon`, `tablespoon` | either, says the spec | a **number** — `chef-lang` prints anything not explicitly liquid as one |

`Fibonacci.chef` declares its three prompt characters in millilitres so they come
out as `N? `, and its `flour` in grams so it comes out as `55`. This recipe wants
every ingredient printed as a letter, and grams are more honest for butter and
flour, so it converts them all at the end instead:

```
Liquefy contents of the mixing bowl.
```

One statement, and the whole bowl turns from thirteen numbers into thirteen
letters. `Liquefy <ingredient>.` does one at a time; `Liquefy contents of the
mixing bowl.` does the lot. Both work in `chef-lang` — checked with a throwaway
recipe of `72 g apples` and `73 g pears`, which prints `H73` when only the apples
are liquefied.

### Backwards, because the dish empties from the top

The bowl is a stack, and the baking dish prints from the top down, so the recipe
stirs the greeting in **reverse**:

```
Put runny honey into the mixing bowl.      bowl: [!]
Put icing sugar into the mixing bowl.      bowl: [!, d]
Put plain flour into the mixing bowl.      bowl: [!, d, l]
...
Put caster sugar into the mixing bowl.     bowl: [!, d, l, r, o, W, ' ', ',', o, l, l, e]
Put butter into the mixing bowl.           bowl: [!, d, l, r, o, W, ' ', ',', o, l, l, e, H]
```

Same reason the garnish goes in last in `Fibonacci.chef`, applied to all thirteen
characters instead of three.

### Ten ingredients, thirteen letters

`plain flour` is stirred in three times and `ground almonds` twice, because
`Hello, World!` has three `l`s and two `o`s and an ingredient can be used as
often as you like — `Put` copies the value rather than consuming it. Shakespeare
needed a stack for the same repeats and Rockstar reused variables; Chef gets it
from the shopping list.

There is no newline in the list. `chef-lang` finishes with a bare `print()`, so
the trailing newline is the interpreter's — see the warts below.

### Verified output

```
$ cook Chef/HelloWorld.chef | xxd
00000000: 4865 6c6c 6f2c 2057 6f72 6c64 210a       Hello, World!.
```

Fourteen bytes, byte-identical to the other four Hello Worlds in this repo.

## `Fibonacci.chef`

```
Ingredients.
78 ml nutmeg oil
63 ml quince juice
32 ml sparkling water
0 g flour
1 g sugar
raisins
```

Six ingredients, four jobs:

| Ingredient | Job |
|---|---|
| `flour` | `a` — the running answer, starts at 0. Dry, so it prints as a number. |
| `sugar` | `b` — the next value up the ladder, starts at 1. |
| `raisins` | the loop counter, N, filled from the refrigerator. No initial value. |
| `nutmeg oil`, `quince juice`, `sparkling water` | 78, 63, 32 — `N`, `?` and a space, in millilitres so they print as characters. |

### The swap, without a temp variable

Shakespeare had to do the `a, b = b, a+b` shuffle arithmetically because it has
no spare variable; LOLCODE and Rockstar just declared one. Chef needs neither,
because the mixing bowl *is* the scratch space:

```
Put flour into the mixing bowl.      bowl: [a]
Add sugar to the mixing bowl.        bowl: [a+b]        (adds to the top)
Put sugar into the mixing bowl.      bowl: [a+b, b]
Fold flour into the mixing bowl.     flour = b          bowl: [a+b]
Fold sugar into the mixing bowl.     sugar = a+b        bowl: []
```

`Fold` pops, so the two folds unload the bowl in the right order and leave it
empty for the next raisin. After N chops, `flour` holds fib(N).

### The garnish goes in last

```
Put flour into the mixing bowl.            bowl: [55]
Put sparkling water into the mixing bowl.  bowl: [55, ' ']
Put quince juice into the mixing bowl.     bowl: [55, ' ', '?']
Put nutmeg oil into the mixing bowl.       bowl: [55, ' ', '?', 'N']
Pour contents of the mixing bowl into the baking dish.
```

The dish prints top-down: `N`, `?`, space, then the dry `55` as a number —
`N? 55`, byte-identical to what the other three languages produce.

### Verified output

```
$ echo 10 | cook Chef/Fibonacci.chef
N? 55
$ echo 0 | cook Chef/Fibonacci.chef
N? 0
$ echo 30 | cook Chef/Fibonacci.chef
N? 832040
$ echo 100 | cook Chef/Fibonacci.chef
N? 354224848179261915075
```

### The same problem, four ways

| | Shakespeare | LOLCODE | Rockstar | Chef |
|---|---|---|---|---|
| Temp variable | none — swap done arithmetically | `nxt` | `the future` | none — the mixing bowl |
| Guard for `n <= 0` | explicit scene-jump guard | explicit `n < 0` guard | free (`while n > 0`) | **impossible** — no conditionals |
| Numeric type | Python ints, unbounded | signed 64-bit, wraps at `n=93` | .NET `decimal`, exact to `n=138` | Python ints, unbounded |
| Prompt before input | yes | yes | yes | no — output is deferred |
| Reads like | a stage play | a cat | a power ballad | a fruitcake |

## Known warts

- **Negative N hangs forever.** With no comparison operator there is nothing to
  guard with: the loop only asks "is `raisins` zero?", and −3 counts down away
  from zero rather than toward it. Confirmed: `echo -3 | cook Fibonacci.chef`
  produced no output and was still spinning when killed after 4 seconds. The
  other three languages all clamp negatives to 0; Chef simply can't.
- **Non-numeric input dumps a Python traceback.** `echo abc | cook …` ends in
  `ValueError: invalid literal for int() with base 10: 'abc'`, straight out of
  the interpreter's `int(input())`.
- **Empty stdin** gives `RuntimeError: Unexpected end of input while reading
  'raisins'`.
- **The trailing newline is the interpreter's, not the recipe's.** `chef-lang`
  ends with a plain `print()`, so you get exactly one `\n` after the number.
  Chef's spec says nothing about a trailing newline, so another implementation
  may not add one.
- **No overflow.** Values are Python integers, so `n=100` and beyond are exact.
  This is the only one of the four programs that never wraps or throws.
- **`chef-lang` 0.1.0 is a partial implementation** and its parser is a stack of
  unanchored regexes — it wants that blank line after `Serves`, and `Divide`
  does float division rather than the spec's integer semantics. This program
  deliberately sticks to the statements it handles correctly.

## Could you actually bake them?

Chef's design principles insist recipes be genuinely preparable, and the
fruitcake is *almost* honest: flour, sugar and raisins are a real start on one.
The nutmeg oil, quince juice and sparkling water, though, are in the list purely
because 78, 63 and 32 are `N`, `?` and a space.

The shortbread does rather better, because character codes for lowercase letters
land between 97 and 122 and grams of baking ingredient land in the same range.
72 g butter, 101 g caster sugar, 108 g plain flour and 111 g ground almonds is a
plausible sweet shortcrust, and 33 g runny honey and 44 g cocoa powder are
plausible things to do to it. The two that give the game away are 87 g
mascarpone, which does not belong in shortbread, and 32 g candied peel, which is
in there because a space is 32. It would bake into *something*.

Both recipes serve 1, which — as the Hello World Souffle also cheerfully admits
— is a lot of food for one person.
