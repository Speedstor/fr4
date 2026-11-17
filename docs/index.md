# FR4 from woven glass cloth

This site is a trail for one job: making a glass and epoxy circuit board from
woven glass cloth, and finding out whether its dielectric constant is even
enough for 10 Gb serial lanes.

!!! warning "Predictions only"

    Nothing here has been made or measured. The trail collects what published
    sources say. The model says what a test panel *should* read. Pressing a
    panel is the only way to find out what is true.

## How the site is laid out

The sidebar has three groups. Open the one you need.

| Group | What is in it | Read it when |
|---|---|---|
| **The trail** | The steps in the order you would do them: cloth, resin, coating, copper, press, measurement | You are deciding what to buy or do next |
| **The model** | A small Python model, explained one piece at a time, with the code beside the words | You want to know what a number means or where it came from |
| **Reference** | The words used here, and a reading list | A term is unfamiliar, or you want the original sources |

## The two things the model found

1. **The weave hardly shows on a thick board.** A wide trace on five plies
   lies across about three yarns and five layers of cloth, so it averages the
   weave away. The weave matters on one thin ply under a narrow trace.
2. **On a hand-coated panel, resin content is the bigger risk.** The cloth
   fixes the glass in each ply, so thickness tells you resin content, and
   resin content sets the dielectric constant.

The numbers are in [What it predicts](model/predictions.md).

## Run the model

```bash
pip install numpy
python -m fr4sim        # prints every prediction on this site
python -m pytest        # checks the model against known cases
```

## Who wrote what

Claude wrote this site and the model on 16 Nov 2026, at Aldrin's request.
The decisions on the [first trail page](trail/decisions.md) are in Aldrin's
words. Everything else is Claude's reading of the sources, and each page
ends with the sources it used.
