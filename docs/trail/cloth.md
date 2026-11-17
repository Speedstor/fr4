# 1. The cloth

Circuit board cloth is a plain weave of E-glass yarn. The **warp** yarns run
along the roll and the **fill** yarns run across it. Each cloth has a style
number.

| Style | Warp x fill, yarns per inch | Dry thickness | Weight |
|---|---|---|---|
| 106 | 56 x 56 | 0.033 mm | about 24 g/m² (from memory) |
| 1080 | 60 x 47 | 0.053 mm | 48 g/m² |
| 2116 | 60 x 58 (from memory; one maker lists the fill at 57 ± 2) | 0.094 mm | 103 to 105 g/m² |
| 7628 | 44 x 31 | 0.17 to 0.185 mm | 203 to 206 g/m² |

## Which to pick

- The open styles, 106 and 1080, are the ones named as worst for skew.
- 2116 is called a compromise.
- Spread glass and style 3313 are reported as good enough for 10 Gb/s.
- For a first panel, 2116 is the middle choice. Five plies give about 0.6 mm.

## Why the cloth matters twice

1. **It sets the pattern** that a narrow trace can fall on or between.
   See [The weave](../model/weave.md).
2. **It fixes the glass in each ply.** Whatever else is in the ply is resin.
   So on a finished panel, thickness tells you resin content.
   See [Resin content](../model/laminate.md).

!!! note "Not found yet"

    Which of these styles can be bought as plain cloth in small amounts.

## Sources

- [Isola, glass fabric table](https://www.isola-group.com/wp-content/uploads/Isola-Glass-Fabric-04_2022.pdf)
- [Intel, glass styles and the compromise choice](https://intel.com/content/www/us/en/docs/programmable/683883/current/fiberglass-weave-composition.html)
- [2116 weight and thickness](https://www.bestpcbs.com/blog/2026/10/2116-glass-cloth/)
- [7628 weight and count](https://www.bestpcbs.com/blog/tag/7628-glass-fabric/)
- [3313 glass at 10 Gb/s, Dataweek](https://www.dataweek.co.za/53649n)
