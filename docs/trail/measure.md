# 6. Measure

The question was whether the dielectric constant is *consistent*. So the
test patterns look for variation, not for one number. A test pattern etched
on a panel is called a **coupon**.

## Coupon A: does it change across the panel?

A two-layer panel about 150 by 150 mm. Five plies of 2116, copper on both
sides, and the bottom left whole as ground.

- **Nine ring resonators** on a 3 by 3 grid.
- Each ring is a 1.25 mm trace. Measured along its middle it is 100 mm
  round, which is a diameter of 31.8 mm.
- Two short feed lines stop just short of the ring, leaving small gaps.

A ring resonates where a whole number of wavelengths fits round it. The
frequency of the peak gives the dielectric constant under that ring. It
needs no phase calibration, only a frequency reading.

**Measure the thickness at each of the nine sites first.** Thickness tells
you resin content, so it predicts which rings should read high and which
low. Write the prediction down, then measure the rings.

## Coupon B: does the weave show?

One ply of 2116, about 0.15 mm thick, copper on both sides.

- Pairs of parallel traces, about 0.25 mm wide and 50 mm long, 0.5 mm apart.
- Pairs at 0°, 5° and 10° to the warp.
- The 0° pair repeated several times, each shifted sideways by about
  0.1 mm, a quarter of the yarn pitch. At 0° the answer depends on where
  the traces fall on the yarns.

Measure the delay of each trace and compare the two of a pair.

## What the two coupons should read

See [What it predicts](../model/predictions.md).

## Two things published about ring resonators

- Couple the ring loosely. One maker's note says the peak should sit 20 dB
  or more below a straight-through line, so the feed lines do not pull the
  resonance.
- It has been done at hobby scale. One student's ring on a paper-based
  board, read with a pocket network analyser, peaked at 2.148 GHz.

??? abstract "Read the code: `fr4sim/coupons.py`"

    ```python
    --8 < --"fr4sim/coupons.py"
    ```

!!! note "Not done yet"

    No layout has been drawn for either coupon.

## Sources

- [Rogers, ring resonators and the two-length method](https://www.rogerscorp.com/-/media/project/rogerscorp/documents/articles/english/advanced-connectivity-solutions/characterizing-circuit-materials-at-mmwave-frequencies.pdf)
- [A student's ring resonator, MIT](https://fab.cba.mit.edu/classes/MAS.862/people/Quentin/project/2_ring.html)
- [Three ways to measure a board's dielectric constant, Hackaday](https://hackaday.com/tag/time-domain)
