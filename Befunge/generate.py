"""Assembler for Fibonacci.bf.

Befunge has no comment syntax, so the layout reasoning has to live here
instead of in the program. See README.md for the full explanation of the
three-phase design (accumulate -> extract digits -> print digits) and why
each phase gets its own pair of rows.

Every phase follows the same loop idiom:

    check row:    >  [test]  !  |
    body row:         [work]           v
    corridor row:  ^ ------------------ <

The IP enters the check row moving right, hits `|`, and branches vertically:
nonzero (from `!`, i.e. "not done yet") sends it UP into a row that has
nothing but blank cells above the check row's own `>` -- which is exactly
where the *previous* phase left its "done" arrival point, so in practice
"continue" and "done" are two different vertical directions out of the same
`|`, one leading into a body row below, the other leading to whatever sits
directly above.

The one wrinkle: the grid is a fixed 80x25 torus (confirmed empirically --
column 80 wraps to column 0, row 25 wraps to row 0), so a design that just
keeps extending one row rightward runs out of room by the third phase. The
"elevator" below (escape right on row 0, descend through blank columns,
turn left, descend again to a small column) exists purely to relocate the
print-back phase onto fresh, narrow rows instead of letting row 0 grow past
column 80.
"""

WIDTH = 80
NROWS = 12

rows = [[' '] * WIDTH for _ in range(NROWS)]


def put(r, c, s):
    for i, ch in enumerate(s):
        assert c + i < WIDTH, f"row {r} would overflow at column {c + i}: {s!r}"
        rows[r][c + i] = ch


# --- Phase 0: read n, print "N? ", stash n/a/b in grid storage --------------
# Storage layout (all at y=9, so "x9" is shorthand below): (0,9)=a, (1,9)=b,
# (2,9)=n, (3,9)=printV (the digit-extraction scratch), (4,9)=digit count.
init = list('"N","?"," ",&29p009p119p')
Ccheck = len(init)
put(0, 0, init)
put(0, Ccheck, 'v')

# --- Phase 1: accumulate fib(n) into a, decrementing n to 0 ----------------
# a starts at fib(0)=0, b at fib(1)=1; each pass sets a,b = b, a+b and n -= 1.
check = list('>29g!|')
Cbranch = Ccheck + len(check) - 1
put(1, Ccheck, check)

put(2, Cbranch, '>')
body = list('19g:09g+19p09p29g1-29p')
put(2, Cbranch + 1, body)
Cbodyend = Cbranch + 1 + len(body)
put(2, Cbodyend, 'v')

put(3, Cbodyend, '<')
put(3, Ccheck, '^')

# fib-done arrival lands back on row 0 at Cbranch, moving up. Row 0 still has
# plenty of column budget here, so just continue rightward into phase 2's
# setup: printV = a, count = 0.
put(0, Cbranch, '>')
extract_setup = list('09g39p049p')
Csetup = Cbranch + 1
put(0, Csetup, extract_setup)
Cext = Csetup + len(extract_setup)
put(0, Cext, 'v')

# --- Phase 2: split a into decimal digits, least-significant first ---------
# Do-while (a number always has at least one digit, even 0): peel off
# printV % 10, divide printV by 10, count += 1, stop once printV hits 0.
put(4, Cext, '>')
extract_body = list('39g25*%39g25*/39p49g1+49p39g!|')
Cextbody_start = Cext + 1
put(4, Cextbody_start, extract_body)
Cextbranch = Cextbody_start + len(extract_body) - 1

put(5, Cextbranch, '<')
put(5, Cext, '^')

# extraction-done arrival lands on row 0 at Cextbranch. This is already close
# to column 80, and the print-back phase needs ~20 more columns -- too wide to
# continue in place. Escape into the elevator instead of growing row 0
# further: turn right into blank space, then down through a column that is
# guaranteed blank on every row the fib/extraction phases used.
put(0, Cextbranch, '>')
Celevator = Cextbranch + 5
put(0, Celevator, 'v')

# Rows 6-7 are deliberately left blank: the elevator column just passes
# through them on its way down.

# Row 8 is the elevator floor: arrive moving down, turn left, cross back to a
# small column, turn down again into fresh, narrow rows for phase 3.
put(8, Celevator, '<')
Csmall = 10
put(8, Csmall, 'v')

# --- Phase 3: pop digits (most significant first) and print each as a char -
# Also a do-while: there's always at least one digit to print.
put(10, Csmall, '>')
printback_body = list('"0"+,49g1-49p49g!|')
Cpbbody_start = Csmall + 1
put(10, Cpbbody_start, printback_body)
Cpbbranch = Cpbbody_start + len(printback_body) - 1

put(11, Cpbbranch, '<')
put(11, Csmall, '^')

# print-back-done arrival lands on row 9 (directly above row 10) at
# Cpbbranch: print the trailing newline and halt.
put(9, Cpbbranch, '>')
finish = list('25*,@')
put(9, Cpbbranch + 1, finish)


if __name__ == '__main__':
    with open('Fibonacci.bf', 'w') as f:
        f.write('\n'.join(''.join(r).rstrip() for r in rows) + '\n')
