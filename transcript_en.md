# Overlap removal — English transcript

## Short clip

0:00 — Title & overview
Overlap removal snaps first, then left-packs each row without changing row assignment. From the triple stack at (4, 2), A stays at 4, B moves to 6, and C moves to 8 on the middle row—legal with displacement 6 and HPWL 32.

0:17 — The big idea
Sort movables by x within each row and place left without overlap. D, E, and F keep their seed roles on other rows. This is the same shelf pack Tetris uses: simple, deterministic, and a good global legalize baseline.

0:33 — Pseudocode
Overlap removal is a two-phase sketch: snap first, then pack each row. Pseudocode makes the phases explicit so you do not merge them into one vague "fix overlaps" bullet. Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

0:54 — Algorithm sketch
Inside each row, sort by x and place left without interval overlap, skipping fixed macro blocks. On the teaching seed that yields A at 4, B at 6, and C at 8 on the middle row, with displacement 6 and HPWL 32.

1:10 — Step 1: Stacked at (4, 2)
The overlap seed piles three width-two cells on the middle row at x = 4. Greedy snap would leave the same conflict; overlap removal snaps first, then packs each row left to right.

1:22 — Step 2: After snap
Snapping the overlap seed does not separate A, B, and C—they remain at (4, 2). Overlap removal keeps their row assignment and resolves x conflicts by packing.

1:35 — Step 3: Per-row pack
On row y = 2, sort by x and place left without overlap: A at 4, B at 6, and C at 8. Each width-2 cell occupies two consecutive sites, so the row is now legal.

1:48 — Step 4: Metrics
Full overlap removal on the seed is legal with total displacement 6 and HPWL 32. D, E, and F never moved from their overlap seed roles.

1:59 — Step 5: Fixed macros untouched
Macro-sized D stays at (8, 4), E at (0, 4), and F at (10, 0). Overlap removal only repacked the crowded middle row; fixed-looking cells on other rows are untouched.

2:13 — Pitfalls
Common traps: assuming snap alone legalizes, forgetting site width when checking overlap, ignoring fixed macro D at (8, 4), reporting HPWL without legality, and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

2:31 — Your turn
Complete the checklist for at least one track, preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.