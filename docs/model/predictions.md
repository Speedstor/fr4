# What it predicts

!!! warning "Written before any panel exists"

    Use these as predictions to test. The model reads low on the dielectric
    constant, so trust the differences more than the absolute values. See
    [Where it is wrong](limits.md).

## 1. The weave hardly shows on a thick board

Skew between two parallel traces, in picoseconds per inch.

| Board | Trace | Along the warp (0°) | Turned 5° or more |
|---|---|---|---|
| Coupon A: 5 plies of 2116, 0.64 mm | 1.2 mm wide | middle 0.16, worst 0.65 | 0.01 or less |
| Coupon B: 1 ply of 2116, 0.15 mm | 0.22 mm | middle 2.2, worst 2.8 | 0.08 or less |
| 1 ply of 1080, 0.08 mm | 0.13 mm | middle 3.7, worst 5.7 | 0.17 or less |
| 2 plies of 1080, 0.17 mm | 0.28 mm | middle 0.9, worst 2.7 | 0.07 or less |
| 1 ply of 7628, 0.22 mm | 0.38 mm | middle 1.2, worst 2.1 | 0.09 or less |

"Middle" is the median of 300 random placements and "worst" is the largest.

What to take from it:

- One published budget is **1 ps per inch** for a 20 inch lane at 10 Gb/s.
  The thick board meets it at any angle. One thin ply along the warp does
  not.
- **Turning the traces 5° takes the skew below what can be measured.**
- On coupon B the predicted difference along the warp is about 4 ps over
  50 mm. That is about 8° of phase at 5 GHz. Turned 5° it is about 0.3°.

## 2. Resin content is the bigger risk on a hand-coated panel

Coupon A, if the resin share drifts across the panel:

| Resin by weight | Thickness | Dielectric constant | Impedance of the 1.25 mm trace | First ring resonance |
|---|---|---|---|---|
| 45% | 0.56 mm | 4.20 | 45.5 Ω | 1.678 GHz |
| 50% | 0.64 mm | 4.08 | 50.0 Ω | 1.710 GHz |
| 55% | 0.73 mm | 3.97 | 55.0 Ω | 1.741 GHz |

What to take from it:

- Ten points of resin drift move the ring by about **63 MHz** and the
  impedance by about **10 Ω**.
- A 1% change in dielectric constant moves the first resonance by 7.5 MHz.
- With a quality factor near 50 the peak is about 34 MHz wide. Finding its
  centre to a tenth of its width would show a change of about half a
  percent. That last figure is an estimate.

## 3. How to use the predictions

1. Measure the thickness at each of the nine sites.
2. From the thickness, write down which rings should read high and low.
3. Measure the rings.
4. Where they disagree, the model is wrong or the panel has something the
   model leaves out, such as voids.

??? abstract "The full printout of `python -m fr4sim`"

    ```text
    --8<-- "docs/model/report.txt"
    ```

To refresh that printout after changing the model:

```bash
python -m fr4sim > docs/model/report.txt
```
