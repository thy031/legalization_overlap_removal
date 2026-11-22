"""Force-directed placement: reference implementation of the lesson's algorithm.

Idea: every free cell is pulled toward the average position of its net neighbours
(plus a weak pull toward the centre). Fixed pads never move.
    target  = (1 - w) * avg(neighbours) + w * centre
    pos[c]  = (1 - alpha) * pos[c] + alpha * target
Report HPWL (half-perimeter wirelength) before and after, with the SAME net model.

Run:  python3 force_directed_place.py
NOTE: this toy netlist will NOT give the video's exact 52 -> 18.7 / golden 14;
those numbers came from the course's own tiny_place.json + checker.
"""
from __future__ import annotations

def hpwl(pos, nets):
    """Sum over nets of (bbox width + bbox height)."""
    total = 0.0
    for net in nets:
        xs = [pos[c][0] for c in net]
        ys = [pos[c][1] for c in net]
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total

def force_place(pos, nets, fixed=(), alpha=0.12, iters=5, center_pull=0.05):
    pos = {c: tuple(p) for c, p in pos.items()}
    nbrs = {c: set() for c in pos}                 # 2-pin view of every net
    for net in nets:
        for a in net:
            nbrs[a].update(b for b in net if b != a)
    cx = sum(p[0] for p in pos.values()) / len(pos)
    cy = sum(p[1] for p in pos.values()) / len(pos)
    for _ in range(iters):                         # each iteration (round)
        new = dict(pos)
        for c in pos:
            if c in fixed or not nbrs[c]:          # pads stay put
                continue
            ax = sum(pos[n][0] for n in nbrs[c]) / len(nbrs[c])
            ay = sum(pos[n][1] for n in nbrs[c]) / len(nbrs[c])
            tx = (1 - center_pull) * ax + center_pull * cx   # tgt = neighbour avg (+ weak centre)
            ty = (1 - center_pull) * ay + center_pull * cy
            new[c] = ((1 - alpha) * pos[c][0] + alpha * tx,  # small step toward tgt
                      (1 - alpha) * pos[c][1] + alpha * ty)
        pos = new                                  # update all cells together
    return pos

if __name__ == "__main__":
    # Same shape as the lesson's picture: A,B bottom; C,D top; F left-middle; E centre
    start = {"A": (0, 0), "B": (20, 0), "C": (0, 20), "D": (20, 20), "E": (10, 10), "F": (0, 10)}
    nets = [("A", "B"), ("A", "F"), ("F", "C"), ("F", "E"), ("A", "E"), ("E", "D"), ("C", "D"), ("B", "D")]
    for a in (0.03, 0.12, 0.5, 0.95):              # alpha: too small ... too big
        end = force_place(start, nets, alpha=a, iters=5)
        print(f"alpha={a:<5} HPWL {hpwl(start, nets):6.1f} -> {hpwl(end, nets):6.1f}")
    for it in (5, 50, 500):                        # many rounds -> everything collapses
        end = force_place(start, nets, alpha=0.12, iters=it)
        print(f"iters={it:<4} HPWL {hpwl(end, nets):6.1f}")
