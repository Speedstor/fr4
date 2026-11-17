# How the model works

The model is a few hundred lines of Python in the `fr4sim` folder. It turns
a description of a panel into the numbers a test should read.

## The chain

```
cloth style + resin content
        │
        ▼
   ply thickness, glass share            laminate.py
        │
        ▼
   dielectric constant of the panel      laminate.py
        │
        ▼
   a trace on the board:                 microstrip.py
   impedance, delay, ring resonance
        │
        ▼
   two traces on the weave: skew         weave.py
```

Each step has its own page in this group, with the code beside it.

| File | What it answers |
|---|---|
| `materials.py` | What numbers does the model assume? |
| `laminate.py` | Given the resin content, how thick is the board and what is its dielectric constant? |
| `microstrip.py` | Given a trace on that board, what are its impedance and delay? |
| `weave.py` | Given the cloth pattern, how different are two neighbouring traces? |
| `coupons.py` | What are the two test patterns? |
| `press.py` | How hard must the press push? |
| `report.py` | Prints every prediction. |

## Run it

```bash
pip install numpy
python -m fr4sim
python -m pytest
```

## What it assumes

Every assumed number is in one file.

| Assumption | Value | Where it comes from |
|---|---|---|
| Dielectric constant of E-glass | 6.4 | Middle of the published range, 6.2 to 6.6 |
| Dielectric constant of cured epoxy | 3.3 | Middle of the published range, 3.0 to 3.6 |
| Density of E-glass | 2.55 g/cm³ | From memory |
| Density of cured epoxy | 1.20 g/cm³ | From memory, for epoxy without bromine |
| Yarn width as a share of yarn spacing | 0.4 to 0.8 by style | A guess |

??? abstract "Read the code: `fr4sim/materials.py`"

    ```python
    --8 < --"fr4sim/materials.py"
    ```

## Units

Millimetres, gigahertz and picoseconds throughout. A name ends in its unit
where there could be doubt, as in `thickness_mm`.
