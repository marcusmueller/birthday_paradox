#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author: Marcus Müller
# License: WTFPL.
from matplotlib import pyplot
import numpy
import typing


N_HASH = 701

def P_collision(n_entries: int, n_candidates: int) -> float:
    return (1 - #calculating the no collisions prob
            numpy.prod(
                numpy.arange(n_entries-n_candidates, n_entries + 1) / # n_candidates factors
                n_entries
            )
    )

n_cands = numpy.arange(1, N_HASH//5)
prob_collision = [P_collision(N_HASH, n) for n in n_cands]

max_below_half = 0
while(prob_collision[max_below_half] < 0.5):
    max_below_half += 1

max_below_ninetynine = max_below_half
while(prob_collision[max_below_ninetynine] < 0.99 and max_below_ninetynine < len(prob_collision)):
    max_below_ninetynine += 1

f= pyplot.figure(figsize=(6,5), dpi=150)
pyplot.axhline(y=0.5, alpha=0.5)
pyplot.axvline(x=n_cands[max_below_half], alpha=0.5, color='orange')
pyplot.axvline(x=n_cands[max_below_ninetynine], alpha=0.5, color='r')
pyplot.semilogy(n_cands, prob_collision)
pyplot.xlabel("Number of PMTs in existence")
pyplot.xlabel("Probability of having at least one collision")
pyplot.title("Probability has no mercy for hashes that have {:d} values".format(N_HASH))
pyplot.yticks(
    sorted([10**n for n in range(int( numpy.log10(prob_collision[0]))-1, 0)] + [1.0, 0.5])
)
ticks = numpy.append(( n_cands[max_below_half], n_cands[max_below_ninetynine]),
        numpy.arange(start=0, stop=N_HASH//2, step=25))
ticks_la = ["P>0.5 @ {:d}".format(ticks[0]), "P>99% @ {:d}".format(ticks[1])] + [str(t) for t in ticks[2:]]

pyplot.xticks(ticks, ticks_la, rotation=45)
pyplot.xlim((n_cands[0], n_cands[-1]))
print ("maximum below 50%: {mbh:d}, below 99%: {mbnn:d}".format(mbnn=max_below_ninetynine, mbh=max_below_half))
pyplot.tight_layout()
f.savefig("why a {:d} hashtable is bad.png".format(N_HASH))
#pyplot.show()

### Check the histogram

occ = numpy.fromfile("histogram.csv", sep="\n", dtype=int)
f= pyplot.figure(figsize=(6,5), dpi=150)
total = occ.sum()
rel = occ.astype(float)/occ.sum()*701
pyplot.plot(rel)
pyplot.title("distribution of hashes")
pyplot.xlabel("hash")
pyplot.ylabel("relative occurence (ideal: 1/701 constant), N = {:d}".format((total)))
pyplot.axhline(rel.mean(),color="b")
pyplot.axhline(rel.mean()+rel.std())
pyplot.axhline(rel.mean()-rel.std())
pyplot.legend(["std: {:f}, mean: {:f}".format(rel.std(), rel.mean())])
f.savefig("distribution of hashes for English words.png")
