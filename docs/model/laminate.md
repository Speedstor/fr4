# Resin content

## The idea

The cloth fixes how much glass is in a ply. A square metre of 2116 cloth
weighs 104 g whatever is done to it. Whatever else is in the ply is resin.

So one number, the resin's share of the weight, sets two things at once:

- **Thickness.** More resin, thicker ply.
- **Dielectric constant.** Glass is about 6.4 and resin about 3.3. More
  resin pulls the mixture down toward 3.3.

That is why a thickness map of a panel is also a map of its dielectric
constant.

## The sums

For one ply, with the cloth's weight `W` in g/m², the resin's share of the
weight `r`, and densities in g/cm³:

```text
glass thickness (µm) = W / glass density
resin thickness (µm) = W × r / (1 − r) / resin density
glass share of volume = glass thickness / (glass + resin thickness)
```

Worked for 2116 cloth at half resin: 104 / 2.55 = 41 µm of glass, and
104 / 1.20 = 87 µm of resin, so a ply of 127 µm that is 32% glass by volume.

## Mixing two materials

There is no single right rule for the dielectric constant of a mixture. The
model carries three:

| Rule | When it is exact | Use |
|---|---|---|
| Parallel | The field runs along layers of the two materials | Upper bound |
| Series | The field crosses one material and then the other | Lower bound |
| Logarithmic | Never exact; sits between the two | The panel value |

## What it gives for 2116 cloth

| Resin by weight | Glass by volume | Ply thickness | Dielectric constant |
|---|---|---|---|
| 40% | 41.4% | 0.099 mm | 4.34 |
| 45% | 36.5% | 0.112 mm | 4.20 |
| 50% | 32.0% | 0.127 mm | 4.08 |
| 55% | 27.8% | 0.147 mm | 3.97 |
| 60% | 23.9% | 0.171 mm | 3.87 |
| 65% | 20.2% | 0.202 mm | 3.77 |

Each extra point of resin lowers the dielectric constant by about 0.023.

??? abstract "Read the code: `fr4sim/laminate.py`"

    ```python
    --8 < --"fr4sim/laminate.py"
    ```
