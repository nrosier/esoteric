# esoteric

> _"Any sufficiently advanced joke is indistinguishable from a compiler."_

A playground for **esoteric programming languages** — the beautiful, useless,
gloriously impractical corner of computer science where languages are designed
to be funny, painful, artistic, or all three at once.

Nothing in this repo is production code. Nothing in this repo _should ever be_
production code. Everything in this repo is Turing complete anyway, which is
the whole joke.

## Why?

Because writing `Fibonacci` in Python takes four lines and teaches you nothing,
whereas writing it as a five-act Shakespearean tragedy where Romeo and Juliet
pass integers between each other in iambic-ish pentameter teaches you exactly
how little a programming language actually needs.

Esoteric languages strip programming down to its weirdest primitives:
- a tape and eight symbols (Brainfuck)
- a 2D grid your instruction pointer bounces around like a pinball (Befunge)
- cows (COW)
- **feelings** (Shakespeare)

Every one of them is a lesson in what "a language" even means, wrapped in a bit.

## House rules

1. **One folder per language.** `Shakespeare/`, `COW/`, `LOLCODE/`, …
2. **Each folder gets a `README.md`** explaining the language, how to run the
   programs, and a short "how this actually works" for anything non-obvious.
3. **Programs must actually run.** No pseudo-esoterica. If it doesn't produce
   the right answer on a real interpreter, it doesn't count.
4. **Comment generously outside the source.** Most of these languages have no
   comment syntax, so the explanation lives in the folder README.
5. **Classic problems only.** Hello World, FizzBuzz, Fibonacci, primes,
   factorial, 99 Bottles, reverse a string. Same problems, absurd solutions.
   Reusing the same handful of problems makes the languages comparable.
6. **Say how to run it on macOS, Linux _and_ Windows.** All three, wherever the
   interpreter allows it. Mark clearly which platforms were actually tested and
   which are upstream's instructions taken on faith. If a platform has no sane
   native route, say so and point at WSL rather than inventing one.

## The roster

### Started

| Language | Folder | Flavour of madness |
|---|---|---|
| Shakespeare | [Shakespeare/](Shakespeare/) | Source code is a stage play. Characters are variables, dialogue is assignment, insults are negative numbers. |
| LOLCODE | [LOLCODE/](LOLCODE/) | 2007 lolcat captions as a grammar. `HAI` … `KTHXBYE`, and arithmetic you have to say out loud. |
| Rockstar | [Rockstar/](Rockstar/) | Programs are power ballads. Numbers are spelled out as lyrics, one digit per word length. |
| Chef | [Chef/](Chef/) | Programs are recipes. Ingredients are variables, mixing bowls are stacks, and there are no conditionals whatsoever. |
| Ook! | [Ook/](Ook/) | Brainfuck for orang-utans. Three words, `Ook.` `Ook?` `Ook!`, in pairs — plus one pair that hands the memory pointer a banana. |

### Programs so far

| Language | Hello World | Fibonacci |
|---|---|---|
| [Shakespeare](Shakespeare/) | [`HelloWorld.spl`](Shakespeare/HelloWorld.spl) | [`Fibonacci.spl`](Shakespeare/Fibonacci.spl) |
| [LOLCODE](LOLCODE/) | [`HelloWorld.lol`](LOLCODE/HelloWorld.lol) | [`Fibonacci.lol`](LOLCODE/Fibonacci.lol) |
| [Rockstar](Rockstar/) | [`HelloWorld.rock`](Rockstar/HelloWorld.rock) | [`Fibonacci.rock`](Rockstar/Fibonacci.rock) |
| [Chef](Chef/) | [`HelloWorld.chef`](Chef/HelloWorld.chef) | [`Fibonacci.chef`](Chef/Fibonacci.chef) |
| [Ook!](Ook/) | [`HelloWorld.ook`](Ook/HelloWorld.ook) | [`Fibonacci.ook`](Ook/Fibonacci.ook) |

Every Hello World prints the same fourteen bytes, `Hello, World!` and a newline.
Every Fibonacci prints `N? ` and then the answer. Verified on a real interpreter
in all ten cases, which is house rule 3 and the only rule that matters.

#### Hello World, five ways

Reusing the same problems is what makes the languages comparable, and Hello World
is the sharpest comparison available precisely because there is no algorithm in
it. Strip out the computing and what's left is how a language *says a letter*:

| | How the greeting is spelled | The three `l`s and two `o`s | Size |
|---|---|---|---|
| Shakespeare | one character code at a time, each built from powers of two, spoken aloud by Juliet | pushed onto her stack, popped back when the letter returns | 23 assignments, 14 `Speak your mind!` |
| LOLCODE | a string literal, glued together with `SMOOSH` | nothing to do; it's a string | 4 statements |
| Rockstar | poetic number literals — the word lengths of the lyrics *are* the codes — then `Cast` | name the same variable again | 10 literals, 3 concatenations |
| Chef | quantities in the ingredient list, `Liquefy`d from numbers into letters | stir the same ingredient in again | 10 ingredients, 13 `Put`s |
| Ook! | eleven tape cells filled by a single multiplication loop | walk back to the cell and print it again | 170 instructions, 340 Ooks |

Three of the five have no strings at all: in Shakespeare, Chef and Ook! the
greeting exists only as numbers, and the letters appear at the moment of
printing. Rockstar *has* string literals and this program refuses to use one.
LOLCODE has them and uses them, which is why LOLCODE is the only one whose Hello
World looks like a Hello World.

The repeated letters are the accidental highlight. Every language handles them,
and no two handle them the same way — a stack, a variable, a shopping list, a
pointer that comes back.

### On the list

| Language | Flavour of madness |
|---|---|
| **COW** | Twelve instructions, all of them variations on `moo`. A Brainfuck derivative for cattle. |
| **Brainfuck** | The canonical one. Eight characters, one tape, infinite regret. A translated one already lurks in [Ook/](Ook/), which doesn't count. |
| **Befunge** | Two-dimensional. The instruction pointer moves in a direction and code can rewrite itself mid-run. |
| **Whitespace** | Only spaces, tabs and newlines are significant. Every other language's source is a valid-ish Whitespace program. |
| **INTERCAL** | 1972's deliberate hostility. Has a `PLEASE` modifier and rejects your program if you grovel too much _or_ too little. |
| **ArnoldC** | `IT'S SHOWTIME` … `YOU HAVE BEEN TERMINATED`. Every keyword is an Arnold quote. |
| **Piet** | Source code is an abstract bitmap. Programs look like Mondrian paintings. |
| **Malbolge** | Designed to be as close to impossible as a language can get. The first program was found by a search algorithm, not written. |
| **Chicken** | The only token is `chicken`. Instructions are encoded by counting them. |
| **Deadfish** | Four commands, no input, overflows constantly. Barely computes. |
| **Emojicode** | 🍇 real 🍇 blocks 🍉 made 🍉 of emoji. Surprisingly complete. |
| **Velato** | Source code is a MIDI file. The program is also a piece of music. |
| **Unlambda** | Pure combinator calculus. No variables at all — just `s`, `k`, and apply. |
| **Befunge-98 / Fungeoids** | Whole family of grid languages. Rabbit hole warning. |
| **GolfScript / Jelly** | Not "funny" esoteric — _terse_ esoteric. Whole programs in a tweet. |

Pull the next one off the list and go.

## Running things

Each language needs its own interpreter, so the actual setup lives in the
per-language README rather than here. What every folder README owes you:

- **All three platforms.** macOS, Linux and Windows, wherever the interpreter
  can manage it. Esoteric interpreters are usually one-person C or Python
  projects with uneven platform support, so "how do I even run this" is the real
  barrier to entry — not the language.
- **Honesty about what was tested.** These repos accumulate copy-pasted install
  commands nobody has ever executed. If a platform's instructions came from
  upstream docs rather than from a terminal, that gets said out loud.
- **The exact interpreter and version.** Esoteric languages are notorious for
  having several mutually incompatible "reference" implementations, and the spec
  is frequently whatever one binary happens to do.
- **A Windows escape hatch.** Plenty of these interpreters are POSIX-flavoured C
  with no Windows build. WSL is a perfectly good answer; pretending `apt` exists
  on Windows is not.

### Current state of play

| Language | macOS | Linux | Windows |
|---|---|---|---|
| [Shakespeare](Shakespeare/) | tested | pip, identical to macOS | pip, pure Python |
| [LOLCODE](LOLCODE/) | tested (`brew`) | build from source | WSL, or a source build |
| [Rockstar](Rockstar/) | tested (prebuilt binary) | prebuilt binary | prebuilt binary |
| [Chef](Chef/) | tested (`pip`) | pip, identical to macOS | pip, pure Python |
| [Ook!](Ook/) | tested (`pip`) | pip, identical to macOS | pip, pure Python |

Only the macOS column has actually been run on this machine — the rest follows
upstream's documented route. Each folder README says which is which.

## License

MIT, see [LICENSE](LICENSE). Yes, these are licensed. No, that does not make
them safe to use.
