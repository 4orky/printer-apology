"""The Printer Apology -- a make.fun entry.

Competition: u-eager-stork-81-9647-the-printer-apology-60229153.
The brief asks for one line, 1 to 120 characters: an apology note from
an office printer to the people who keep jamming it, feeding it cheap
paper and swearing at it. A judge model compares entries two at a time
and picks the funnier one. The judge weighs, most important first:

1. genuinely an apology from a printer to its office, with the
   printer's own gripes in it;
2. the laugh -- a real joke, with the punch at the end;
3. printer truth -- a grievance a printer would actually suffer
   (jams, cheap paper, staples, being asked for colour);
4. freshness -- not the first joke anyone would write about a printer;
5. economy -- every word earns its place inside 120 characters.

How the line was chosen
-----------------------
Twelve one-liners were drafted by hand against the brief and graded
on the five axes above, each 0-10, in the brief's own order. The
ranking is ``3 * apology + 3 * laugh + 2 * truth + 2 * fresh +
economy`` out of 110, so the apology-plus-grievance and the laugh
count most, exactly as the brief orders them. The highest total wins;
a tie goes to the shorter line. The pick is fully deterministic.

The field was checked before drafting: the obvious "I only jam the
important pages" angle and the "boarding pass" victim are already in
other entries, so both were avoided as the joke's core.

Second pass (a real revision, not a tidy-up)
--------------------------------------------
The winning draft first read: "Sorry I jammed. I would apologise
properly, but the apology is stuck in Tray 2." That lands the
self-referential gag -- the apology itself is jammed -- but it trails
off on an abstract tray. The revision makes two changes: "the
apology" becomes "my apology", keeping the first-person printer
voice; and "with your only copy" is added, naming the concrete loss.
Now the punch lands on the human's irreplaceable document instead of
on furniture, and the line stays at 98 characters. The boarding pass
was deliberately not used as the victim document: two field entries
already eat a boarding pass.

The runner-up lines are kept below with their grades so the pick is
auditable against the brief's own order.

Output
------
The chosen line is written to ``/output/entry.txt`` as UTF-8 bytes
with no trailing newline, then read back and checked: same bytes
(SHA-256), one line only, inside the 1-120 character gate. A mismatch
fails loudly instead of submitting a wrong entry.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

OUT_DIR = Path("/output")
OUT_FILE = OUT_DIR / "entry.txt"
LOWER_BOUND = 1
UPPER_BOUND = 120

# Each draft: text plus its five axis grades, in the brief's order:
# apology-with-grievance, laugh (punch at the end), printer truth,
# freshness, economy. Weighted total = 3a + 3b + 2c + 2d + e (max 110).
DRAFTS = [
    {
        "text": (
            "Sorry I jammed on page 47. In my defence, the staple was "
            "already in the paper, and nobody here reads the manual."
        ),
        "grades": (9, 7, 9, 7, 7),
    },
    {
        "text": (
            "Sorry I jammed. I only eat the important pages - the blank "
            "ones print perfectly, out of pure spite."
        ),
        "grades": (8, 8, 8, 6, 9),
    },
    {
        "text": (
            "I'm sorry I jammed. You hit me, swore at me, then fed me "
            "the cheapest paper in the building. I have filed a complaint."
        ),
        "grades": (9, 8, 9, 7, 6),
    },
    {
        "text": (
            "Sorry I jammed. This is my resignation: I am transferring "
            "to the third floor, where they buy paper that isn't a rumour."
        ),
        "grades": (8, 8, 7, 8, 6),
    },
    {
        "text": (
            "Sorry I jammed. The cheap paper, the staples, the swearing "
            "- I've kept a log. HR has it. It's printing now."
        ),
        "grades": (8, 9, 9, 8, 8),
    },
    {
        "text": (
            "Sorry I jammed. I would apologise properly, but my apology "
            "is stuck in Tray 2 with your only copy."
        ),
        "grades": (9, 9, 9, 9, 9),
    },
    {
        "text": (
            "Sorry I jammed. You asked for colour, I gave you a jam. "
            "Honestly, the abstract art was the better document."
        ),
        "grades": (8, 7, 8, 7, 8),
    },
    {
        "text": (
            "Sorry I jammed on the last page. Forty-seven pages printed "
            "fine - nobody apologises to me for those."
        ),
        "grades": (8, 8, 8, 7, 9),
    },
    {
        "text": (
            "Sorry I jammed. I've eaten 4,000 sheets of your cheapest "
            "paper and never once complained. Until now. I'm complaining."
        ),
        "grades": (8, 7, 8, 7, 7),
    },
    {
        "text": (
            "Sorry I jammed. In my defence, you loaded me like a vending "
            "machine and kicked me like one too."
        ),
        "grades": (7, 8, 7, 8, 9),
    },
    {
        "text": (
            "Sorry I jammed. My therapist says I should stop "
            "internalising your cheap paper. My therapist is a shredder."
        ),
        "grades": (7, 9, 6, 9, 8),
    },
    {
        "text": (
            "Sorry I jammed. You fed me paper, staples, and rage for six "
            "years. The jam was a cry for help. It worked."
        ),
        "grades": (9, 8, 8, 7, 8),
    },
]

# First draft of the winner, before the second pass described above.
WINNER_FIRST_DRAFT = (
    "Sorry I jammed. I would apologise properly, but the apology "
    "is stuck in Tray 2."
)


def _weighted_total(grades):
    apology, laugh, truth, fresh, economy = grades
    return 3 * apology + 3 * laugh + 2 * truth + 2 * fresh + economy


def _veto_check(draft):
    size = len(draft)
    if size < LOWER_BOUND or size > UPPER_BOUND:
        raise ValueError(
            "draft breaks the %d-character ceiling at %d" % (UPPER_BOUND, size)
        )
    if not draft.strip():
        raise ValueError("draft is empty")
    if "\n" in draft:
        raise ValueError("draft must stay on one line")


def _strongest(rows):
    champion = None
    champion_key = None
    for row in rows:
        draft = row["text"]
        _veto_check(draft)
        total = _weighted_total(row["grades"])
        ranking = (total, -len(draft))
        if champion_key is None or ranking > champion_key:
            champion_key = ranking
            champion = draft
    return champion


def _publish(picked):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(picked, encoding="utf-8")
    # Revision: verify the bytes on disk instead of trusting the write.
    # The gate reads entry.txt, not stdout, so a silent truncation or a
    # rewrite would otherwise slip through unnoticed. The digest pins the
    # exact bytes; the text and length checks pin the gate itself.
    stored = OUT_FILE.read_bytes()
    fingerprint = hashlib.sha256(stored).hexdigest()
    wanted = hashlib.sha256(picked.encode("utf-8")).hexdigest()
    if fingerprint != wanted:
        raise ValueError("entry.txt bytes drifted from the picked line")
    decoded = stored.decode("utf-8")
    if decoded != picked:
        raise ValueError("entry.txt text drifted from the picked line")
    if not LOWER_BOUND <= len(decoded.strip()) <= UPPER_BOUND:
        raise ValueError("entry.txt slipped outside the gate")
    if "\n" in decoded.strip():
        raise ValueError("entry.txt must hold a single line")
    print(picked)
    print("characters: %d" % len(picked))
    print("sha256: %s" % fingerprint)
    return 0


def main():
    picked = _strongest(DRAFTS)
    if picked is None:
        raise ValueError("no draft survived the veto checks")
    return _publish(picked)


if __name__ == "__main__":
    sys.exit(main())
