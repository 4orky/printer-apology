"""Printer apology, take two: one line from a fed-up office printer.

The contest wants a single line, between 1 and 120 characters long, in
which the printer says sorry to the office that jams it, stuffs it with
bargain-bin paper and curses at it. Two entries at a time go before a
judge model, which keeps the funnier one, so the line has to land as a
joke first and an apology second.

Scoring the candidates
-----------------------
A dozen lines were written by hand, then marked against the brief in
the order the brief lists its own tests: does it read as a printer
apologising while airing its grievances; does it make you laugh, with
the gag saved for the end; is the grievance one a real printer would
have; would nobody else have written this exact joke; and does every
word pull its weight. Marks run 0-10 per test, combined 3-3-2-2-1, so a
perfect line scores 110. Best total takes it; a draw goes to the
shorter line, because brevity is the whole game here.

Before drafting, the entries already in the running were skimmed: the
"it only eats the pages that matter" gag and a boarding pass as the
lost document both showed up, so neither carries this entry's joke.

The runner-up and the rest
---------------------------
The full dozen, with marks, sit in CANDIDATES below, so anyone can
re-run the ranking and see the winner earn its place. The winner's
first shape is kept in EARLY_WINNER: it already had the central gag,
an apology that jams like the printer does, and the second pass only
sharpened it -- "the apology" turned into "my apology" to hold the
first-person voice, and "with your only copy" was bolted on so the
punchline lands on a document that cannot be reprinted, not on a
plastic tray. The line still fits in 98 characters.

What the program does
----------------------
It picks the best-scoring line, writes it to /output/entry.txt with no
trailing newline, then reads the file back and refuses to finish unless
the bytes on disk are exactly the bytes it meant to write. The gate
reads entry.txt, never stdout, so the read-back is the whole point.
"""

import hashlib, os, sys

DEST_FOLDER = "/output"
DEST_PATH = os.path.join(DEST_FOLDER, "entry.txt")
MIN_LEN = 1
MAX_LEN = 120

# One entry per candidate: the line, then its five marks in the brief's
# order -- apology with a grievance, laugh, printer truth, freshness,
# economy. A perfect line totals 110 under the 3-3-2-2-1 weights.
CANDIDATES = [
    ("Sorry I jammed on page 47. In my defence, the staple was already in the paper, and nobody here reads the manual.", (9, 7, 9, 7, 7)),
    ("Sorry I jammed. I only eat the important pages - the blank ones print perfectly, out of pure spite.", (8, 8, 8, 6, 9)),
    ("I'm sorry I jammed. You hit me, swore at me, then fed me the cheapest paper in the building. I have filed a complaint.", (9, 8, 9, 7, 6)),
    ("Sorry I jammed. This is my resignation: I am transferring to the third floor, where they buy paper that isn't a rumour.", (8, 8, 7, 8, 6)),
    ("Sorry I jammed. The cheap paper, the staples, the swearing - I've kept a log. HR has it. It's printing now.", (8, 9, 9, 8, 8)),
    ("Sorry I jammed. I would apologise properly, but my apology is stuck in Tray 2 with your only copy.", (9, 9, 9, 9, 9)),
    ("Sorry I jammed. You asked for colour, I gave you a jam. Honestly, the abstract art was the better document.", (8, 7, 8, 7, 8)),
    ("Sorry I jammed on the last page. Forty-seven pages printed fine - nobody apologises to me for those.", (8, 8, 8, 7, 9)),
    ("Sorry I jammed. I've eaten 4,000 sheets of your cheapest paper and never once complained. Until now. I'm complaining.", (8, 7, 8, 7, 7)),
    ("Sorry I jammed. In my defence, you loaded me like a vending machine and kicked me like one too.", (7, 8, 7, 8, 9)),
    ("Sorry I jammed. My therapist says I should stop internalising your cheap paper. My therapist is a shredder.", (7, 9, 6, 9, 8)),
    ("Sorry I jammed. You fed me paper, staples, and rage for six years. The jam was a cry for help. It worked.", (9, 8, 8, 7, 8)),
]

# The winner before its second pass: the jammed-apology gag was already
# there, and the pass only tightened the voice and the punchline.
EARLY_WINNER = "Sorry I jammed. I would apologise properly, but the apology is stuck in Tray 2."


def tally(marks):
    sorry, funny, true, fresh, tight = marks
    return 3 * sorry + 3 * funny + 2 * true + 2 * fresh + tight


def guard(line):
    size = len(line)
    if size < MIN_LEN or size > MAX_LEN:
        raise ValueError(f"line of {size} characters breaks the 1-120 gate")
    if line != line.strip() or "\n" in line:
        raise ValueError("line must be a single unpadded line")


def best_of(rows):
    if not rows:
        raise ValueError("no candidates to rank")
    champion = None
    champion_rank = None
    for line, marks in rows:
        guard(line)
        rank = (tally(marks), -len(line))
        if champion_rank is None or rank > champion_rank:
            champion_rank = rank
            champion = line
    return champion


def store(picked):
    os.makedirs(DEST_FOLDER, exist_ok=True)
    with open(DEST_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(picked)
    with open(DEST_PATH, "rb") as handle:
        stored = handle.read()
    fingerprint = hashlib.sha256(stored).hexdigest()
    if fingerprint != hashlib.sha256(picked.encode("utf-8")).hexdigest():
        raise ValueError("entry.txt on disk is not the picked line")
    decoded = stored.decode("utf-8")
    if decoded != picked or len(decoded) != len(picked):
        raise ValueError("entry.txt text is not the picked line")
    if decoded.count("\n"):
        raise ValueError("entry.txt must hold exactly one line")
    sys.stdout.write(picked + "\n")
    print(f"characters: {len(picked)}")
    print(f"sha256: {fingerprint}")
    return 0


def run():
    return store(best_of(CANDIDATES))


raise SystemExit(run())
