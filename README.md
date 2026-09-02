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

## The roster

### Started

| Language | Folder | Flavour of madness |
|---|---|---|
| Shakespeare | [Shakespeare/](Shakespeare/) | Source code is a stage play. Characters are variables, dialogue is assignment, insults are negative numbers. |
| LOLCODE | [LOLCODE/](LOLCODE/) | 2007 lolcat captions as a grammar. `HAI` … `KTHXBYE`, and arithmetic you have to say out loud. |

### On the list

| Language | Flavour of madness |
|---|---|
| **COW** | Twelve instructions, all of them variations on `moo`. A Brainfuck derivative for cattle. |
| **Brainfuck** | The canonical one. Eight characters, one tape, infinite regret. |
| **Befunge** | Two-dimensional. The instruction pointer moves in a direction and code can rewrite itself mid-run. |
| **Whitespace** | Only spaces, tabs and newlines are significant. Every other language's source is a valid-ish Whitespace program. |
| **INTERCAL** | 1972's deliberate hostility. Has a `PLEASE` modifier and rejects your program if you grovel too much _or_ too little. |
| **Chef** | Programs are recipes. They must be valid programs _and_ plausible food. |
| **Rockstar** | Programs are power ballads. Written so devs could legitimately call themselves rockstar developers. |
| **ArnoldC** | `IT'S SHOWTIME` … `YOU HAVE BEEN TERMINATED`. Every keyword is an Arnold quote. |
| **Ook!** | Brainfuck for orang-utans. Three tokens: `Ook.`, `Ook?`, `Ook!` |
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

Each language needs its own interpreter, so setup lives in the per-language
README rather than here. General approach:

- Prefer a **pip / npm / brew installable interpreter** so the folder README can
  give a one-line install.
- Note the exact interpreter and version used, since esoteric languages are
  notorious for having several mutually incompatible "reference"
  implementations.
- Where an online interpreter exists, link it too — sometimes that's the whole
  install story.

## License

MIT, see [LICENSE](LICENSE). Yes, these are licensed. No, that does not make
them safe to use.
