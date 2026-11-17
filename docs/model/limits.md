# Where it is wrong

A model is useful when you know how it fails. This one fails in these ways.

## It reads low

Against one maker's figure of 4.49 at 1 GHz and 56% resin, the model gives
3.95. That is 12% low.

Likely reasons: the maker's resin is a brominated epoxy with a higher
dielectric constant than the 3.3 assumed here, and the mixing rule is only
a rule of thumb.

**So use the model for differences, not for absolute values.** With the
maker's 4.49, coupon A's first ring resonance would be near 1.64 GHz
and not 1.71 GHz.

## It reads thick

Against a maker's 2116 ply of 0.119 mm at 52% resin, the model gives
0.135 mm. That is 13% thick.

Likely reasons: the resin density assumed here is for epoxy without
bromine, and in a real press some resin flows out at the edges.

## The yarn widths are guesses

How wide a yarn is, as a share of the spacing between yarns, sets how much
the weave shows. The model uses 0.4 for 106, 0.5 for 1080, 0.7 for 2116 and
0.8 for 7628. None of these is from a data sheet. A microscope photo of the
real cloth would replace them.

## The skew table is not the worst case

Along the warp, skew depends on the spacing of the two traces against the
spacing of the yarns. The table uses 0.5 mm. The worst spacing would put
one trace on a yarn and the other on a gap.

## It knows nothing about making

Voids, resin flow, uneven cure, and resin that is thicker on one side of
the panel are where a real panel will differ. None of them is in the model.
Only pressing a panel will show them.

## How to correct it

After the first panel, three numbers can be replaced with measurements:

1. The resin's dielectric constant, from one ring and one thickness.
2. The resin's density, from a weighed and measured offcut.
3. The yarn widths, from a photo of the cloth.

All three are in `fr4sim/materials.py`.
