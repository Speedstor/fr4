# The weave

## The idea

Glass has a higher dielectric constant than resin. A trace that runs along a
yarn sits over more glass than one that runs along a gap between yarns, so
its signal is slower. The difference in arrival time between the two traces
of a pair is the **skew**.

## The model in four steps

1. **Yarns are lenses of glass.** Each yarn is drawn as a lens-shaped
   bundle. Warp yarns run along x and fill yarns along y.
2. **Plies are shifted at random.** Nobody lines the plies up, so each one
   gets a random sideways shift.
3. **Under each point, glass and resin are stacked.** The field under a
   trace runs down through the board, so the two mix by the series rule.
4. **The trace averages.** It averages what lies under its width, and its
   delay is the average along its length.

Then it repeats the whole thing 300 times with new random shifts, because
nobody controls where a trace lands on the cloth. The result is a spread of
skews, not one number.

## Two rules it keeps

- **It moves glass around but adds none.** The yarn heights are set so the
  average over the cloth equals the glass the cloth really has. A test
  checks this.
- **Same seed, same answer.** The random numbers are seeded, so a run can be
  repeated exactly.

## What it leaves out

- The up-and-down waviness of the yarns as they cross.
- Voids.
- The field that spreads beyond the edges of the trace.
- Real yarn widths. The width of a yarn as a share of yarn spacing is a
  guess for each style.

## Why a thick board hides the weave

Three kinds of averaging stack up:

| Averaging | Thick board, wide trace | One thin ply, narrow trace |
|---|---|---|
| Across the trace width | 1.25 mm covers about three yarns | 0.22 mm covers half a yarn |
| Through the plies | Five plies at random shifts | One ply |
| Along the length | Only if the trace is turned against the yarns | The same |

??? abstract "Read the code: `fr4sim/weave.py`"

    ```python
    --8 < --"fr4sim/weave.py"
    ```
