# A trace on the board

## The idea

A **microstrip** is a trace on top of the board with a ground plane
underneath. Part of its field is in the board and part is in the air above.
So the signal sees an *effective* dielectric constant, written `eps_eff`,
somewhere between 1 and the board's own value.

Two numbers follow from it:

- **Delay.** The signal travels at the speed of light divided by the square
  root of `eps_eff`.
- **Impedance.** Set mostly by the ratio of trace width to board thickness.

The model uses the closed-form formulas of Hammerstad and Jensen from 1980.
They ignore how the values creep with frequency.

## Three ways to read a board with it

**A ring resonator.** A ring resonates where a whole number of wavelengths
fits round it:

```text
resonance n = n × speed of light / (distance round the ring × √eps_eff)
```

with `n` a whole number. Measure the peak, and `eps_eff_from_ring` gives
`eps_eff` back.

**Two lines of different length.** Measure the phase through each and
subtract. The connectors cancel, and what is left belongs to the extra
length alone. `eps_eff_from_two_lengths` does the sum.

**Impedance.** A thicker or thinner board shows up here first. On coupon A,
5% more thickness moves a 50 Ω trace by about 1.5 Ω.

## A check against a familiar board

A 3 mm trace on a 1.6 mm board with a dielectric constant of 4.4 is the
textbook 50 Ω line. The model gives a value within 2 Ω of that, and a test
holds it there.

??? abstract "Read the code: `fr4sim/microstrip.py`"

    ```python
    --8 < --"fr4sim/microstrip.py"
    ```
