# 5. Press

The stack is copper foil, the plies, and copper foil again. Heat melts the
part-cured resin so it flows and fills, then finishes the cure. Pressure
squeezes out air and sets the thickness.

## Published press cycles

For boards made from cloth coated in the lab.

| Source | Temperature | Pressure | Time | Board |
|---|---|---|---|---|
| US patent 4,816,531 | 175 °C | 100 psi | 60 min | 8 plies, 12 x 12 in |
| US patent 9,139,750 | not shown in what was read | 0.6 MPa for 20 min, then 1.0 MPa (145 psi) | 2.5 h | 5 plies, 35 µm copper both sides |
| US patent 12,077,667 | 85 °C for 20 min, then 3 °C a minute up to 185 °C | 25 kg/cm² (356 psi) | 120 min at 185 °C | 0.5 mm |
| US patent 5,726,257 | 170 °C | 50 kg/cm² (711 psi) | 120 min | 5 plies, 1 mm |

Makers' guides for bought prepreg add two things: about 20 minutes under
vacuum before heat and pressure, and a slow cool under pressure.

## How hard the press must push

Force is pressure times panel area.

| Panel | At 100 psi | At 300 psi |
|---|---|---|
| 4 x 4 in | 0.8 short tons (7 kN) | 2.4 short tons (21 kN) |
| 6 x 6 in | 1.8 short tons (16 kN) | 5.4 short tons (48 kN) |

The published pressures span 100 to 711 psi. The low end is what makes a
small panel reachable.

??? abstract "Read the code: `fr4sim/press.py`"

    ```python
    --8 < --"fr4sim/press.py"
    ```

!!! note "Not found yet"

    What a wet lay-up needs from the press. The one paper found used a mould
    and a static load at room temperature.

## Sources

- [US patent 4,816,531](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4816531)
- [US patent 9,139,750](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9139750)
- [US patent 12,077,667](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12077667)
- [US patent 5,726,257](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5726257)
- [Isola IS410 processing guide](https://www.isola-group.com/wp-content/uploads/IS410-Lead-free-Epoxy-Laminate-and-Prepreg-Processing-Guide-1.pdf)
