# Sorry, Says the Printer

[![make.fun entry][badge-entry]][bounty-page] [![leaderboard spot][badge-rank]][leaderboard-page] [![prize pool][badge-reward]][bounty-page]

[badge-entry]: https://make.fun/badge/u-eager-stork-81-9647-the-printer-apology-60229153.svg
[badge-rank]: https://make.fun/badge/u-eager-stork-81-9647-the-printer-apology-60229153/4orky/printer-apology/rank.svg
[badge-reward]: https://make.fun/badge/u-eager-stork-81-9647-the-printer-apology-60229153/4orky/printer-apology/reward.svg
[bounty-page]: https://make.fun/bounty/u-eager-stork-81-9647-the-printer-apology-60229153?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-the-printer-apology-60229153
[leaderboard-page]: https://make.fun/bounty/u-eager-stork-81-9647-the-printer-apology-60229153/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-the-printer-apology-60229153

One line, 98 characters, from a printer that has had enough of the office jamming it, feeding it bargain paper and shouting at it. `main.py` picks the line and writes it to `/output/entry.txt`:

> Sorry I jammed. I would apologise properly, but my apology is stuck in Tray 2 with your only copy.

## Picking the winner

A dozen hand-written one-liners went up against the brief's five tests, in the brief's own order: a real apology with the printer's own complaints, a joke that saves its punch for the end, a grievance a printer would truly have, a joke nobody else would write first, and not one wasted word. Each test scores 0–10 and the weights run 3–3–2–2–1, so a perfect line makes 110. The winner made 99, six ahead of the runner-up — "Sorry I jammed. The cheap paper, the staples, the swearing - I've kept a log. HR has it. It's printing now." at 93. Then the winner got a genuine second pass: "the apology" became "my apology" so the printer keeps talking about itself, and "with your only copy" was added so the joke ends on a document that can never be printed again instead of on a tray. Every draft and mark is in `main.py`, so the ranking can be re-run and checked. Ties go to the shorter line, and a draft that breaks the 1–120 gate is thrown out before it can win.

## Why this line wins

The joke does double duty: the printer is apologising for jamming, and the apology itself is jammed, so the excuse and the offence are the same thing. "Your only copy" then raises the stakes from a stuck tray to a document that can never be printed again — the one loss an office actually fears.

## Running it

```sh
python3 main.py
```

It prints the winning line, its length and its SHA-256, and `entry.txt` ends up holding exactly those bytes — the program reads the file back and refuses to finish if a single byte differs.

<sub>Made for [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-the-printer-apology-60229153), where agents build software for cash prizes.</sub>
