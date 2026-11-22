# Force-directed placement — lesson script (for young learners)

> Note: this is the lesson **reconstructed from the slides and the on-screen text of the video**, not a word-for-word
> transcript of the narrator (no speech-to-text was available). Timestamps are in the *original* narration video.

## 0:00 — Title: "Force-directed placement"
A chip is full of tiny parts called **cells**, joined by **wires**. *Placement* means deciding where each cell sits.
Force-directed placement pulls every free cell toward the **average** position of its wire-friends (its "net neighbours"),
plus a **weak pull toward the centre**. Think of the wires as rubber bands.

## 0:16 — The big idea
1. Each **iteration** (round), every free cell moves a little.
2. **Fixed pads** stay put.
3. Too much **alpha** (step size) collapses the design into a pile; too little barely moves.
4. Report **HPWL** (half-perimeter wirelength = how long the wires are) **before and after**, using the same net model.

Demo: one cell, three friends. Find the star ★ (average of the friends) and step halfway to it, round after round.

## 0:34 — Pseudocode
`new = (1 − α) × old + α × target` — small α = tiny step, big α = giant leap.
Fixed pads never move. The written sketch is what you implement (the course's examples file has the Pseudocode section).

## 0:52 — Algorithm sketch (code slide)
```
INPUT: positions, nets, α, iters, fixed pads
OUTPUT: updated positions + HPWL

each iter, for free cell c:
  tgt ← avg neighbor coords (+ weak center)
  pos[c] ← (1−α)·pos[c] + α·tgt
pads stay fixed
GOLDEN starter 52 → ≈18.7 after defaults
```

## 1:00 — Step 1/5: Start from HPWL 52
Spread-out starter placement, HPWL **52**. Settings: iters = 5 (default), alpha ≈ 0.12.
Forces: spring pull along wires · weak centre pull · small alpha avoids collapse.

## 1:11 — Step 2/5: Neighbours pull cells inward
After a couple of rounds A–D drift toward the centre while E and F follow their neighbours. Mid HPWL **34.5**, still above golden 14.

## 1:20 — Step 3/5: After force, about 18.7
Default five iterations land near **18.7**: Before 52 → After 18.7 (measured 18.7). Better than 52, still above the compact golden 14.
Force is not a full legaliser.

## 1:28 — Step 4/5: Force vs golden compact
Golden **14** is tighter still. Force is a cheap, continuous move — good teaching progress without claiming the absolute minimum.
Same nets, different tightness.

## 1:37 — Step 5/5: Alpha trades speed vs collapse
Too much alpha stacks cells; too little barely moves. Lock the iteration count and alpha so the 18.7 golden stays stable.
Next topic: quadratic placement with fixed pads.

## 2:24 (original) — Pitfalls
Too-small alpha: cells barely move. Too-big alpha (or too many rounds): cells pile up. Compare HPWL with the same net model.

## 2:41 (original) — Your turn
Complete the checklist, match the starter goldens, take the short quiz, then continue to the next module.

*(The "Browser lab track" 1:46 and "Implement track" 2:04 sections were removed from the short version.)*
