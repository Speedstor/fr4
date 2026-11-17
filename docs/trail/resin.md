# 2. The resin

## What "FR4" means

FR-4 is the flame retardant grade of glass and epoxy laminate. The same
laminate without a flame retardant is called G-10. Makers of FR-4 get the
flame rating from bromine built into the epoxy, at 19 to 22% by weight.

A board made with ordinary epoxy is G-10 in kind. For a test of the
dielectric constant that difference is small. For a product it is not.

## Three ways to put epoxy on the cloth

Most hazardous first.

### Route 1: hardener dissolved in dimethylformamide

This is the common industrial recipe: brominated epoxy, dicyandiamide as the
hardener, and an imidazole to speed it. Dicyandiamide barely dissolves in
acetone, methyl ethyl ketone or alcohols, which is why a strong solvent is
used.

!!! danger "Leave this route out"

    Dimethylformamide is on the European Chemicals Agency's list of substances
    of very high concern, as toxic for reproduction. Its classification
    carries the statement "May damage the unborn child".

### Route 2: a varnish without dimethylformamide

Two published kinds.

- **The same hardener in a milder solvent.** One patent example, by weight:
  57.2% brominated epoxy, 1.7% dicyandiamide, 26.8% propylene glycol
  monomethyl ether and 14.3% acetone, with 0.1% 2-methylimidazole on solids.
  Another patent calls the hardener's solubility in that ether very low, so
  the sources disagree on how well this works.
- **A different hardener** that dissolves in methyl ethyl ketone.
  Phenolic-cured FR-4 is sold as "non-dicy".

Either way an oven boils a flammable solvent off the cloth.

### Route 3: liquid epoxy with no solvent, laid up wet

This is how glass and epoxy laminates are made by hand. Resin is worked into
each ply and the stack is pressed while it cures. One paper pressed eight
plies in a mould, cured them 48 hours at room temperature and then 2 hours at
80 °C. A vacuum bag over the wet stack raises the glass content and lowers
voids.

!!! note "Not found yet"

    - A wet-laid board clad in copper, with a measured dielectric constant.
    - Whether a room-temperature epoxy stands up to soldering.

## Not checked for any route

The hazards of the other solvents, of the resins and of the hardeners. From
memory, epoxy resins and amine hardeners sensitise skin. Read each safety
data sheet before buying anything.

## Sources

- [Norplex-Micarta, G-10 against FR-4, and the bromine share](https://www.norplex-micarta.com/wp-content/uploads/2018/08/G10_G11_applications_VS_FR-4_FR-5.pdf)
- [Norplex-Micarta, what G-10 is](https://www.norplex-micarta.com/structural-materials/what-is-g-10/)
- [European Chemicals Agency, dimethylformamide on the candidate list](https://echa.europa.eu/candidate-list-table/-/dislist/details/0b0236e1807dec94)
- [US patent 5,407,977, solubility of dicyandiamide](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5407977)
- [US patent 4,816,531, varnish in the milder solvent](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4816531)
- [US patent 9,215,803, hardeners that dissolve in methyl ethyl ketone](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9215803)
- [NCAB, "dicy" and "non-dicy" FR-4](https://www.ncabgroup.com/it/faq/dicy-and-nondicy/)
- [Hand lay-up with room temperature cure](https://arxiv.org/pdf/2406.15292)
- [Wet lay-up with a vacuum bag](https://app.jove.com/t/65376/measuring-mechanical-properties-glass-fiber-reinforcement-polymer)
